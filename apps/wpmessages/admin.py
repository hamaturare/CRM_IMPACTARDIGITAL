from django.contrib import admin
from .models import WpMessage

class WpMessageAdmin(admin.ModelAdmin):
    list_display = ('lead_phone_number', 'profile_name', 'message_timestamp', 
                    'business_phone_number', 'state', 'service_interest', 
                    'contact_method', 'chat_history')
    list_filter = ('lead_phone_number', 'profile_name','state', 'service_interest', 'contact_method')

admin.site.register(WpMessage, WpMessageAdmin)
