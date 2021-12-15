"""Unit tests for the Club model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Club

class ClubModelTestCase(TestCase):
    """Unit tests for the Club model."""

    def setUp(self):
        self.club = Club.objects.create_club(
            club_name = 'Club X',
            club_location = 'London',
            club_description = 'The club description',
        )

    def test_club_name_must_not_be_blank(self):
        self.club.club_name = ''
        self._assert_club_model_is_invalid()

    def test_club_name_may_contain_50_characters(self):
        self.club.club_name = 'x' * 50
        self.club.club_location = 'London'
        self.club.club_description = 'The club desc'
        self._assert_club_model_is_valid()

    def test_club_name_must_not_contain_more_than_50_characters(self):
        self.club.club_name = 'x' * 51
        self._assert_club_model_is_invalid()

    def test_club_location_must_not_be_blank(self):
        self.club.club_location = ''
        self._assert_club_model_is_invalid()

    def test_club_location_may_contain_100_characters(self):
        self.club.club_location = 'x' * 100
        self.club.club_name = 'Club X'
        self.club.club_description = 'The club desc'
        self._assert_club_model_is_valid()

    def test_club_location_must_not_contain_more_than_100_characters(self):
        self.club.club_location = 'x' * 101
        self._assert_club_model_is_invalid()

    def test_club_description_must_not_be_blank(self):
        self.club.club_description = ''
        self._assert_club_model_is_invalid()

    def test_club_description_may_contain_520_characters(self):
        self.club.club_description = 'x' * 520
        self.club.club_name = 'Club X'
        self.club.club_location = 'London'
        self._assert_club_model_is_valid()

    def test_club_description_must_not_contain_more_than_520_characters(self):
        self.club.club_description = 'x' * 521
        self._assert_club_model_is_invalid()

    def _assert_club_model_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_club_model_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()
