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


class Upcoming_patients(models.Model):
    UID = models.CharField(max_length=10, primary_key=True)
    Scheduled_date = models.DateField()


class ins_Policy(models.Model):
    plan = models.CharField(max_length=20, primary_key=True)


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


class Patients(models.Model):
    Name = models.CharField(max_length=150)
    Street = models.CharField(max_length=150)
    City = models.CharField(max_length=150)
    State = models.CharField(max_length=150)
    Pin = models.IntegerField()
    UID = models.CharField(max_length=10, primary_key=True)
    Disatisfy = models.CharField(max_length=100, default="", null=True)
    Current = models.IntegerField(null=True)
    Book_Date = models.DateTimeField(null=True, blank=True)
    Limit = models.IntegerField()
    Coinsurance = models.IntegerField()
    Deduct_Paid = models.IntegerField()
    Limit_Left = models.IntegerField()


    created_at = models.DateTimeField(default=timezone.now)

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

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.UID:
            self.slug = slugify(self.Name)

        return super(Patients, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listing',
                       args=[self.slug])