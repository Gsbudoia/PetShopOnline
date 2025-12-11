from django.contrib import admin
from .models import ServiceType, Appointment

admin.site.register(ServiceType)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('pet', 'date', 'vet')
    list_filter = ('date',)