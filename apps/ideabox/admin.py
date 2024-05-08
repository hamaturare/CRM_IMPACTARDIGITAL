from django.contrib import admin
from .models import Priority

# Register your models here.


class PriorityAdmin(admin.ModelAdmin):
    list_display = ['name']  # Mostra o nome no painel admin
    search_fields = ['name']  # Permite buscar por nome


admin.site.register(Priority, PriorityAdmin)

