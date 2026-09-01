from django.db import models


class AuthorizedEmail(models.Model):
    normalized_email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["normalized_email"]

    def save(self, *args, **kwargs):
        self.normalized_email = self.normalized_email.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.normalized_email

