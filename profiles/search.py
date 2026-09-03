SEARCHABLE_FIELDS = (
    "full_name",
    "country_of_origin",
    "previous_employment",
    "undergraduate_institution",
    "desired_industry",
    "hobbies",
    "linkedin_url",
)


def _searchable_text(profile):
    return " ".join(getattr(profile, field) or "" for field in SEARCHABLE_FIELDS).lower()


def search_profiles(profiles, query):
    """Filter an iterable of Profile objects to those matching every word in query."""
    query_words = query.lower().split()
    if not query_words:
        return list(profiles)

    return [
        profile
        for profile in profiles
        if all(word in _searchable_text(profile) for word in query_words)
    ]
