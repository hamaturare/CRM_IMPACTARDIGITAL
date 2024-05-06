from django.db import models
from django.utils.translation import gettext_lazy as _

class ServiceType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Serviço Prestado"))

    def __str__(self):
        return self.name

class Client(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Dia que a Lead Chegou"))
    client_name = models.CharField(max_length=255, verbose_name=_("Nome do Cliente"), blank=True)
    company_name = models.CharField(max_length=255, verbose_name=_("Nome da Empresa"), blank=True)
    contract_date = models.DateField(verbose_name=_("Data do Contrato"),null=True, blank=True)
    next_contact_date = models.DateField(verbose_name=_("Data próximo Contato"),null=True, blank=True)
    email = models.EmailField(max_length=255, unique=False, verbose_name=_("Email"), blank=True)
    instagram = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Instagram"))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    whatsapp = models.CharField(max_length=20, verbose_name=_("Whatsapp (Telefone)"), blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, verbose_name=_("Tipos de Serviço da Lead"))
    # Continuação dos outros campos
    city = models.CharField(max_length=50, verbose_name=_("Cidade"), blank=True)
    state = models.CharField(max_length=2, verbose_name=_("Estado"), blank=True)
    client_kpis = models.CharField(max_length=50, verbose_name=_("KPIs"), blank=True)
    client_income = models.CharField(max_length=50, verbose_name=_("Valor do Contrato"), blank=True)
    client_budget = models.CharField(max_length=50, verbose_name=_("Gasto Máximo Mensal"), blank=True)
    client_info = models.TextField(max_length=500, blank=True)
    

    def __str__(self):
        return '%s %s' % (self.client_name, self.company_name)
