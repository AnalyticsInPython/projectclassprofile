from django.test import TestCase
from django.utils import timezone

from profiles.models import Profile
from profiles.search import search_profiles


class SearchProfilesTests(TestCase):
    def setUp(self):
        self.jenny = Profile.objects.create(
            full_name="Jenny Tran",
            cbs_email="jenny@example.edu",
            country_of_origin="Vietnam",
            previous_employment="Consulting",
            linkedin_url="https://www.linkedin.com/in/jennytran",
            consent_confirmed_at=timezone.now(),
        )
        self.david = Profile.objects.create(
            full_name="David Lee",
            cbs_email="david@example.edu",
            country_of_origin="United States",
            previous_employment="Senior Financial Analyst",
            linkedin_url="https://www.linkedin.com/in/davidlee",
            consent_confirmed_at=timezone.now(),
        )

    def test_empty_query_returns_all_profiles_unfiltered(self):
        results = search_profiles(Profile.objects.all(), "")
        self.assertEqual(set(results), {self.jenny, self.david})

    def test_matches_by_partial_name(self):
        results = search_profiles(Profile.objects.all(), "jenny")
        self.assertEqual(results, [self.jenny])

    def test_matches_by_country(self):
        results = search_profiles(Profile.objects.all(), "vietnam")
        self.assertEqual(results, [self.jenny])

    def test_matches_by_previous_employment(self):
        results = search_profiles(Profile.objects.all(), "financial analyst")
        self.assertEqual(results, [self.david])

    def test_matches_by_linkedin_url(self):
        results = search_profiles(Profile.objects.all(), "davidlee")
        self.assertEqual(results, [self.david])

    def test_search_is_case_insensitive(self):
        results = search_profiles(Profile.objects.all(), "JENNY")
        self.assertEqual(results, [self.jenny])

    def test_multiple_words_require_all_to_match(self):
        results = search_profiles(Profile.objects.all(), "david vietnam")
        self.assertEqual(results, [])

    def test_typo_does_not_match(self):
        results = search_profiles(Profile.objects.all(), "jeny")
        self.assertEqual(results, [])

    def test_unrelated_query_returns_no_results(self):
        results = search_profiles(Profile.objects.all(), "xyzzy nonexistent")
        self.assertEqual(results, [])
