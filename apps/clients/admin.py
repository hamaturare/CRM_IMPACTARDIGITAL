from django.contrib import admin
from .models import Client, ServiceType

def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None  # Ao setar o id como None, um novo id será atribuído na criação da cópia.
        object.save()

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']  # Mostra o nome no painel admin
    search_fields = ['name']  # Permite buscar por nome

class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'company_name', 'email','created_at')
    list_filter = ('client_name', 'company_name', 'created_at', )  # Filtros na barra lateral
    search_fields = ('client_name', 'company_name', 'email')
    actions = [duplicate_record]

admin.site.register(Client, ClientAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)