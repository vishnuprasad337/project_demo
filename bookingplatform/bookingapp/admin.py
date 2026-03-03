from django.contrib import admin
from .models import Hotel,Hotelbooking,Room

admin.site.register(Hotel)
admin.site.register(Room)


@admin.register(Hotelbooking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'room_type', 'check_in', 'total_amount')
    list_filter = ('room_type', 'check_in')
    search_fields = ('name', 'email')

