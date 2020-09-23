# Generated by Django 3.0.4 on 2020-09-18 21:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20200909_0154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=150)),
                ('Street', models.CharField(max_length=150)),
                ('City', models.CharField(max_length=150)),
                ('State', models.CharField(max_length=150)),
                ('Pin', models.IntegerField()),
                ('UID', models.CharField(max_length=10)),
                ('Deduct', models.IntegerField()),
                ('Copay', models.IntegerField()),
                ('Limit', models.IntegerField()),
                ('Coinsurance', models.IntegerField()),
                ('Deduct_Paid', models.IntegerField()),
                ('Limit_Left', models.IntegerField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('flagged', models.BooleanField(default=False)),
                ('flagged_at', models.DateTimeField(blank=True, null=True)),
                ('flagged_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
    ]