from django.db import models
from django.utils.timezone import now
from django.db.models import URLField


class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        LAYOFFS = "Layoffs"
        HIRING_FREEZE = "Hiring Freeze"
        HIRING = "Hiring"

    name = models.CharField(max_length=300, unique=True)
    status = models.CharField(max_length=300, choices=CompanyStatus.choices, default=CompanyStatus.HIRING)
    last_update = models.DateTimeField(default=now, editable=True)
    application_link = URLField(blank=True)
    notes = models.CharField(max_length=300, blank=True)