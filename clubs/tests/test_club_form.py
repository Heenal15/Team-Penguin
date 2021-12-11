""" Unit tests for the club form """
from django import forms
from django.test import TestCase
from clubs.forms import ClubForm
from clubs.models import Club

class ClubFormTestCase(TestCase):
    """ Unit tests for the club form """

    def setUp(self):
        self.form_input = {'club_name': 'Club X', 'club_location': 'London', 'club_description': 'The club description'}

    def test_form_has_necessary_fields(self):
        form = ClubForm()
        self.assertIn('club_name', form.fields)
        self.assertIn('club_location', form.fields)
        self.assertIn('club_description', form.fields)

    def test_valid_club_form(self):
        form = ClubForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_in_valid_club_information_form(self):
        self.form_input['club_name'] = ""
        self.form_input['club_description'] = ""
        self.form_input['club_location'] = ""
        form = ClubForm(data=self.form_input)
        self.assertFalse(form.is_valid())
