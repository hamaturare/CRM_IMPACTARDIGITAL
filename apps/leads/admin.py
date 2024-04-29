from django.contrib import admin
from .models import Lead, ServiceType

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']  # Mostra o nome no painel admin
    search_fields = ['name']  # Permite buscar por nome

class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'objective', 'priority', 'created_at')
    list_filter = ('priority', 'created_at', 'objective')  # Filtros na barra lateral
    search_fields = ('first_name', 'last_name', 'email')

admin.site.register(Lead, LeadAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
