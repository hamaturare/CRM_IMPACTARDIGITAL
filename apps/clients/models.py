from django.db import models
from django.utils.translation import gettext_lazy as _

class ServiceType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Serviço Prestado"))

    def __str__(self):
        return self.name

class Client(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Dia que a Lead Chegou"))
    client_name = models.CharField(max_length=255, verbose_name=_("Nome do Cliente"), blank=True)
    date_of_birth = models.DateField(verbose_name=_("Data de Aniversário do Cliente"),null=True, blank=True)
    company_name = models.CharField(max_length=255, verbose_name=_("Nome da Empresa"), blank=True)
    contract_date = models.DateField(verbose_name=_("Data do Contrato"),null=True, blank=True)
    next_contact_date = models.DateField(verbose_name=_("Data próximo Contato"),null=True, blank=True)
    email = models.EmailField(max_length=255, unique=False, verbose_name=_("Email"), blank=True)
    instagram = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Instagram"))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    whatsapp = models.CharField(max_length=20, verbose_name=_("Whatsapp (Telefone)"), blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, verbose_name=_("Serviços do Cliente"))
    city = models.CharField(max_length=50, verbose_name=_("Cidade"), blank=True)
    status = models.BooleanField(default=False)  
    client_kpis = models.CharField(max_length=50, verbose_name=_("KPIs"), blank=True)
    client_income = models.CharField(max_length=50, verbose_name=_("Valor do Contrato"), blank=True)
    client_budget = models.CharField(max_length=50, verbose_name=_("Gasto Máximo Mensal"), blank=True)
    client_info = models.TextField(max_length=2500, blank=True, verbose_name=_("Informações Sobre o Cliente"))
    

    def __str__(self):
        return '%s %s' % (self.client_name, self.company_name)

class ClientLeads(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name=_("Cliente Associado"))
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Data da Indicação"))
    name = models.CharField(max_length=255, verbose_name=_("Nome da Lead"), blank=True)    
    company_name = models.CharField(max_length=255, verbose_name=_("Empresa da Lead"), blank=True)
    whatsapp = models.CharField(max_length=20, verbose_name=_("Whatsapp (Telefone)"), blank=True)
    email = models.EmailField(max_length=255, unique=False, verbose_name=_("Email"), blank=True)
    notes = models.TextField(max_length=50, blank=True, verbose_name=_("Anotações"))

    def __str__(self):
        return f"Nome: {self.name} Empresa: {self.company_name}"