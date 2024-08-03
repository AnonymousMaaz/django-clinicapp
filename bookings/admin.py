from django.contrib import admin

# Register your models here.
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'status', 'booked_at')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'date', 'time')
