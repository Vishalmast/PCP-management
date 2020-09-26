from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Patient(models.Model):
    UID = models.CharField(max_length=10, primary_key=True)
    Name = models.CharField(max_length=150)
    Street = models.CharField(max_length=150)
    City = models.CharField(max_length=150)
    State = models.CharField(max_length=150)
    Pin = models.IntegerField()
    Insurance_policy_plan = models.CharField(max_length=30, default='')
    out_of_pocket_limit = models.IntegerField()
    Limit_left = models.IntegerField()
    Copay = models.IntegerField()
    Coinsurance = models.FloatField()
    Deductible = models.IntegerField()
    Deduct_Paid = models.IntegerField()
    Current = models.IntegerField(null=True, blank=True)
    Disatisfy = models.CharField(max_length=100, default="", null=True, blank=True)

    # Book_Date = models.DateTimeField(null=True, blank=True)

    flagged = models.BooleanField(default=False)
    flagged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    flagged_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.Name


class Upcoming(models.Model):
    UID = models.ForeignKey(Patient, on_delete=models.CASCADE)
    Scheduled_date = models.DateField()
    Payment_by_payer = models.FloatField()
    Payment_by_dependant = models.FloatField()


