from django.shortcuts import get_object_or_404, render
from registrar.models.portfolio import Portfolio
from waffle.decorators import flag_is_active


def index_organizations(request, portfolio_id):
    """This page is available to anyone without logging in."""
    context = {}

    if request.user.is_authenticated:
        # This is a django waffle flag which toggles features based off of the "flag" table
        context["has_profile_feature_flag"] = flag_is_active(request, "profile_feature")
        context["has_organization_feature_flag"] = flag_is_active(request, "organization_feature")

        # Retrieve the portfolio object based on the provided portfolio_id
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        context["portfolio"] = portfolio
        
        # This controls the creation of a new domain request in the wizard
        request.session["new_request"] = True

        print('homepage organizations view')

    return render(request, "home_organizations.html", context)

def organization_domains(request, portfolio_id):
    context = {}

    if request.user.is_authenticated:
        # This is a django waffle flag which toggles features based off of the "flag" table
        context["has_profile_feature_flag"] = flag_is_active(request, "profile_feature")
        context["has_organization_feature_flag"] = flag_is_active(request, "organization_feature")

        # Retrieve the portfolio object based on the provided portfolio_id
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        context["portfolio"] = portfolio
        context["content"] = "domains"

        # This controls the creation of a new domain request in the wizard
        request.session["new_request"] = True

        print('organization domains view')

    return render(request, "home_organizations.html", context)

def organization_domain_requests(request, portfolio_id):
    context = {}

    if request.user.is_authenticated:
        # This is a django waffle flag which toggles features based off of the "flag" table
        context["has_profile_feature_flag"] = flag_is_active(request, "profile_feature")
        context["has_organization_feature_flag"] = flag_is_active(request, "organization_feature")

        # Retrieve the portfolio object based on the provided portfolio_id
        portfolio = get_object_or_404(Portfolio, id=portfolio_id)
        context["portfolio"] = portfolio
        context["content"] = "domain-requests"

        # This controls the creation of a new domain request in the wizard
        request.session["new_request"] = True

        print('organization domain requests view')

    return render(request, "home_organizations.html", context)