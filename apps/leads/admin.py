from django.contrib import admin
from .models import Lead, ServiceType

def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None  # Ao setar o id como None, um novo id será atribuído na criação da cópia.
        object.save()

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']  # Mostra o nome no painel admin
    search_fields = ['name']  # Permite buscar por nome

class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'priority', 'created_at')
    list_filter = ('priority', 'created_at', )  # Filtros na barra lateral
    search_fields = ('first_name', 'last_name', 'email')
    actions = [duplicate_record]

admin.site.register(Lead, LeadAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
