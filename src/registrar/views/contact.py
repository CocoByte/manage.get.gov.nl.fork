from waffle.decorators import waffle_flag
from urllib.parse import urlencode, urlunparse, urlparse, quote
from django.urls import NoReverseMatch, reverse
from registrar.forms.contact import ContactForm
from registrar.models.contact import Contact
from registrar.templatetags.url_helpers import public_site_url
from registrar.views.utility.permission_views import ContactPermissionView
from django.views.generic.edit import FormMixin
from registrar.models.utility.generic_helper import to_database, from_database
from django.utils.safestring import mark_safe

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

import logging

logger = logging.getLogger(__name__)


class BaseContactView(ContactPermissionView):
    """Provides a base view for the contact object. On get, the contact
    is saved in the session and on self.object."""
    def get(self, request, *args, **kwargs):
        """Sets the current contact in cache, defines the current object as self.object
        then returns render_to_response"""
        self._set_contact(request)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def _set_contact(self, request):
        """
        get contact from session cache or from db and set
        to self.object
        set session to self for downstream functions to
        update session cache
        """
        self.session = request.session

        contact_pk = "contact:" + str(self.kwargs.get("pk"))
        cached_contact = self.session.get(contact_pk)

        if cached_contact:
            self.object = cached_contact
        else:
            self.object = self.get_object()

        self._update_session_with_contact()

    def _update_session_with_contact(self):
        """
        Set contact pk in the session cache
        """
        contact_pk = "contact:" + str(self.kwargs.get("pk"))
        self.session[contact_pk] = self.object


class ContactFormBaseView(BaseContactView, FormMixin):
    """Adds a FormMixin to BaseContactView, and handles post"""
    def post(self, request, *args, **kwargs):
        """Form submission posts to this view.

        This post method harmonizes using BaseContactView and FormMixin
        """
        # Set the current contact object in cache
        self._set_contact(request)

        form = self.get_form()

        # Get the current form and validate it
        return self.form_valid(form) if form.is_valid() else self.form_invalid(form)

    def form_invalid(self, form):
        # updates session cache with contact
        self._update_session_with_contact()

        # superclass has the redirect
        return super().form_invalid(form)


class ContactProfileSetupView(ContactFormBaseView):
    """This view forces the user into providing additional details that 
    we may have missed from Login.gov"""
    template_name = "finish_contact_setup.html"
    form_class = ContactForm
    model = Contact

    redirect_type = None

    # TODO - make this an enum
    class RedirectType:
        """
        Contains constants for each type of redirection.
        Not an enum as we just need to track string values,
        but we don't care about enforcing it.

        - HOME: We want to redirect to reverse("home")
        - BACK_TO_SELF: We want to redirect back to reverse("finish-contact-profile-setup")
        - TO_SPECIFIC_PAGE: We want to redirect to the page specified in the queryparam "redirect"
        - COMPLETE_SETUP: Indicates that we want to navigate BACK_TO_SELF, but the subsequent
        redirect after the next POST should be either HOME or TO_SPECIFIC_PAGE
        """
        HOME = "home"
        BACK_TO_SELF = "back_to_self"
        COMPLETE_SETUP = "complete_setup"
        TO_SPECIFIC_PAGE = "domain_request"

    # TODO - refactor
    @waffle_flag('profile_feature')
    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):

        # Default redirect type
        default_redirect = self.RedirectType.BACK_TO_SELF

        # Update redirect type based on the query parameter if present
        redirect_type = request.GET.get("redirect", None)

        is_default = False
        # We set this here rather than in .get so we don't override
        # existing data if no queryparam is present.
        if redirect_type is None:
            is_default = True
            redirect_type = default_redirect

            # Set the default if nothing exists already
            if self.redirect_type is None:
                self.redirect_type = redirect_type

        if not is_default:
            default_redirects = [
                self.RedirectType.HOME,
                self.RedirectType.COMPLETE_SETUP,
                self.RedirectType.BACK_TO_SELF,
                self.RedirectType.TO_SPECIFIC_PAGE
            ]
            if redirect_type not in default_redirects:
                self.redirect_type = self.RedirectType.TO_SPECIFIC_PAGE
                request.session["profile_setup_redirect_viewname"] = redirect_type
            else:
                self.redirect_type = redirect_type

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        """
        Returns a URL string based on the current value of self.redirect_type.

        Depending on self.redirect_type, constructs a base URL and appends a 
        'redirect' query parameter. Handles different redirection types such as 
        HOME, BACK_TO_SELF, COMPLETE_SETUP, and TO_SPECIFIC_PAGE.

        Returns:
            str: The full URL with the appropriate query parameters.
        """
        base_url = ""
        query_params = {}
        match self.redirect_type:
            case self.RedirectType.HOME:
                base_url = reverse("home")
            case self.RedirectType.BACK_TO_SELF | self.RedirectType.COMPLETE_SETUP:
                base_url = reverse("finish-contact-profile-setup", kwargs={"pk": self.object.pk})
            case self.RedirectType.TO_SPECIFIC_PAGE:

                # We only allow this session value to use viewnames,
                # because otherwise this allows anyone to enter any value in here.
                # This restricts what can be redirected to.
                try:
                    desired_view = self.session["profile_setup_redirect_viewname"]
                    base_url = reverse(desired_view)
                except NoReverseMatch as err:
                    logger.error(err)
                    logger.error(
                        "ContactProfileSetupView -> get_redirect_url -> Could not find specified page."
                    )
                    base_url = reverse("home")
            case _:
                base_url = reverse("home")
        
        # Quote cleans up the value so that it can be used in a url
        query_params["redirect"] = quote(self.redirect_type)

        # Parse the base URL
        url_parts = list(urlparse(base_url))

        # Update the query part of the URL
        url_parts[4] = urlencode(query_params)

        # Construct the full URL with query parameters
        full_url = urlunparse(url_parts)
        return full_url

    def get_success_url(self):
        """Redirect to the nameservers page for the domain."""
        redirect_url = self.get_redirect_url()
        return redirect_url

    # TODO - delete session information
    def post(self, request, *args, **kwargs):
        """Form submission posts to this view.

        This post method harmonizes using BaseContactView and FormMixin
        """

        # Set the current contact object in cache
        self._set_contact(request)

        form = self.get_form()

        # Get the current form and validate it
        if form.is_valid():
            if "contact_setup_save_button" in request.POST:
                # Logic for when the 'Save' button is clicked
                self.redirect_type = self.RedirectType.COMPLETE_SETUP
            elif "contact_setup_submit_button" in request.POST:
                if "profile_setup_redirect_viewname" in self.session:
                    self.redirect_type = self.RedirectType.TO_SPECIFIC_PAGE
                else:
                    self.redirect_type = self.RedirectType.HOME

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        
        completed_states = [
            self.RedirectType.TO_SPECIFIC_PAGE,
            self.RedirectType.HOME
        ]
        if self.redirect_type in completed_states:
            self.request.user.finished_setup = True
            self.request.user.save()
        
        to_database(form=form, obj=self.object)
        self._update_session_with_contact()

        return super().form_valid(form)
    
    def get_initial(self):
        """The initial value for the form (which is a formset here)."""
        db_object = from_database(form_class=self.form_class, obj=self.object)
        return db_object
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["email_sublabel_text"] = self._email_sublabel_text()

        if self.redirect_type == self.RedirectType.COMPLETE_SETUP:
            context["confirm_changes"] = True

        return context
    
    def _email_sublabel_text(self):
        """Returns the lengthy sublabel for the email field"""
        help_url = public_site_url("help/account-management/#get-help-with-login.gov")
        return mark_safe(
            "We recommend using your work email for your .gov account. "
            "If the wrong email is displayed below, you’ll need to update your Login.gov account "
            f'and log back in. <a class="usa-link" href={help_url}>Get help with your Login.gov account.</a>'
        )
