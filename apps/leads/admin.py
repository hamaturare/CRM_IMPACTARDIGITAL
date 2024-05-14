from django.contrib import admin
from .models import Lead, ServiceType, Priority, Origin, FollowUp

def duplicate_record(modeladmin, request, queryset):
    for object in queryset:
        object.id = None  # Ao setar o id como None, um novo id será atribuído na criação da cópia.
        object.save()

class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'company_name', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('first_name', 'company_name', 'email')
    actions = [duplicate_record]

    class FollowUpInline(admin.TabularInline):  # Inlines dentro da classe LeadAdmin
        model = FollowUp
        extra = 1  # Define quantos campos vazios de FollowUp aparecerão por padrão

    inlines = [FollowUpInline]  # Adiciona o inline à configuração do admin de Lead
    
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class OriginAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

# Removendo FollowUpAdmin como admin independente, já que será usado como inline
# Se você ainda quer ter acesso direto ao Admin de FollowUps, você pode manter esta classe e a chamada a admin.site.register abaixo

# class FollowUpAdmin(admin.ModelAdmin):
#     list_display = ['lead', 'planned_date', 'actual_date', 'notes']
#     list_filter = ['planned_date', 'actual_date']
#     search_fields = ['notes', 'lead__first_name', 'lead__company_name']

admin.site.register(Lead, LeadAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Priority, PriorityAdmin)
admin.site.register(Origin, OriginAdmin)
# admin.site.register(FollowUp, FollowUpAdmin)  # Remover se os FollowUps serão exclusivamente inlines de Lead
