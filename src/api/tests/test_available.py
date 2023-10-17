"""Test the available domain API."""

import json

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory

from ..views import available, _domains, in_domains
from .common import less_console_noise
from registrar.tests.common import MockEppLib
from unittest.mock import MagicMock, patch, call

from epplibwrapper import (
    commands,
    common,
    extensions,
    responses,
    RegistryError,
    ErrorCode,
)

API_BASE_PATH = "/api/v1/available/"
from registrar.models import Domain

class AvailableViewTest(MockEppLib):

    """Test that the view function works as expected."""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create(username="username")
        self.factory = RequestFactory()

    def test_view_function(self):
        request = self.factory.get(API_BASE_PATH + "test.gov")
        request.user = self.user

        response = available(request, domain="test.gov")
        # has the right text in it
        self.assertContains(response, "available")
        # can be parsed as JSON
        response_object = json.loads(response.content)
        self.assertIn("available", response_object)

    def test_makes_calls(self):
        gsa_available = in_domains("gsa.gov")
        igorville_available = in_domains("igorvilleremixed.gov")

        self.mockedSendFunction.assert_has_calls(
            [
                call(
                    commands.CheckDomain(
                        ["gsa.gov"],
                    ),
                    cleaned=True,
                ),
                call(
                    commands.CheckDomain(
                        ["igorvilleremixed.gov"],
                    ),
                    cleaned=True,
                )
            ]
        )

    def test_in_domains(self):
        gsa_available = in_domains("gsa.gov")
        gsa_caps_available = in_domains("GSA.gov")
        igorville_available = in_domains("igorvilleremixed.gov")
        
        self.assertTrue(gsa_available)
        # input is lowercased so GSA.GOV should be found
        self.assertTrue(gsa_caps_available)
        # This domain should not have been registered
        self.assertFalse(igorville_available)
            
    def test_in_domains_dotgov(self):
        gsa_available = in_domains("gsa.gov")
        gsa_caps_available = in_domains("GSA.gov")
        igorville_available = in_domains("igorvilleremixed.gov")

        """Domain searches work without trailing .gov"""
        self.assertTrue(in_domains("gsa"))
        # input is lowercased so GSA.GOV should be found
        self.assertTrue(in_domains("GSA"))
        # This domain should not have been registered
        self.assertFalse(in_domains("igorvilleremixed"))

    def test_in_domains_capitalized(self):
        gsa_available = in_domains("gsa.gov")
        capitalized_gsa_available = in_domains("GSA.gov")

        """Domain searches work without case sensitivity"""
        self.assertTrue(in_domains("gsa.gov"))
        self.assertTrue(in_domains("GSA.gov"))

    def test_not_available_domain(self):
        """gsa.gov is not available"""
        request = self.factory.get(API_BASE_PATH + "gsa.gov")
        request.user = self.user
        response = available(request, domain="gsa.gov")
        self.assertFalse(json.loads(response.content)["available"])

    def test_available_domain(self):
        """igorvilleremixed.gov is still available"""
        request = self.factory.get(API_BASE_PATH + "igorvilleremixed.gov")
        request.user = self.user
        response = available(request, domain="igorvilleremixed.gov")
        self.assertTrue(json.loads(response.content)["available"])

    def test_available_domain_dotgov(self):
        """igorvilleremixed.gov is still available even without the .gov suffix"""
        request = self.factory.get(API_BASE_PATH + "igorvilleremixed")
        request.user = self.user
        response = available(request, domain="igorvilleremixed")
        self.assertTrue(json.loads(response.content)["available"])

    def test_error_handling(self):
        """Calling with bad strings raises an error."""
        bad_string = "blah!;"
        request = self.factory.get(API_BASE_PATH + bad_string)
        request.user = self.user
        response = available(request, domain=bad_string)
        self.assertFalse(json.loads(response.content)["available"])
        # domain set to raise error successfully raises error
        with self.assertRaises(RegistryError):
            error_domain_available = available(request, "errordomain.gov")


class AvailableAPITest(MockEppLib):

    """Test that the API can be called as expected."""

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create(username="username")

    def test_available_get(self):
        self.client.force_login(self.user)
        response = self.client.get(API_BASE_PATH + "nonsense")
        self.assertContains(response, "available")
        response_object = json.loads(response.content)
        self.assertIn("available", response_object)

    def test_available_post(self):
        """Cannot post to the /available/ API endpoint."""
        # have to log in to test the correct thing now that we require login
        # for all URLs by default
        self.client.force_login(self.user)
        with less_console_noise():
            response = self.client.post(API_BASE_PATH + "nonsense")
        self.assertEqual(response.status_code, 405)
