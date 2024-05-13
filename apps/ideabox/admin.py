from django.contrib import admin
from .models import Priority, Suggestion, Status

class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'priority', 'get_username')
    list_filter = ('priority', 'created_at', 'user')
    search_fields = ('title', 'user__username', 'content', 'priority__name')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

admin.site.register(Priority, PriorityAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Suggestion, SuggestionAdmin)
