from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'selected_package',
        'starting_location', 'travel_date',
        'nights', 'adults', 'children',
        'hotel_category', 'transportation',
        'travel_group',
        'created_at'
    )

    search_fields = ('name', 'phone', 'selected_package')
    list_filter = ('hotel_category', 'travel_group', 'transportation')
    ordering = ('-created_at',)
