from django.contrib import admin
from django.utils import timezone

from .models import Category, Patients
from .models import *


class PatientAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Street', 'City', 'State', 'Pin', 'UID', 'Current', 'Book_Date', 'Disatisfy', 'Limit', 'Coinsurance', 'Deduct_Paid', 'Limit_Left', 'flagged', 'flagged_by', 'flagged_at')
    list_filter = ('Book_Date',)
    exclude = ['slug', 'created_at', 'flagged_at', 'flagged_by']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        if obj.flagged:
            obj.flagged_by = request.user
            obj.flagged_at = timezone.now()
        else:
            obj.flagged_by = obj.flagged_at = None

        super().save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Patients, PatientAdmin)
admin.site.register(Patient)
admin.site.register(ins_Policy)
admin.site.register(Upcoming_patients)