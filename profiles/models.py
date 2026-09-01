from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_linkedin_url


class Profile(models.Model):
    full_name = models.CharField(max_length=200)
    cbs_email = models.EmailField(unique=True)
    photo = models.ImageField(
        upload_to="profile_photos/",
        blank=True,
        null=True,
    )
    country_of_origin = models.CharField(max_length=120, blank=True)
    previous_employment = models.CharField(max_length=240, blank=True)
    undergraduate_institution = models.CharField(max_length=240, blank=True)
    desired_industry = models.CharField(max_length=200, blank=True)
    hobbies = models.TextField(blank=True)
    age = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)],
    )
    linkedin_url = models.URLField(blank=True, validators=[validate_linkedin_url])
    consent_confirmed_at = models.DateTimeField()

    class Meta:
        ordering = ["full_name"]

    def save(self, *args, **kwargs):
        self.cbs_email = self.cbs_email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
