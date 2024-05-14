from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Origin(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Origem da Lead"))

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Prioridade"))

    def __str__(self):
        return self.name

class ServiceType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Serviço de Interesse"))

    def __str__(self):
        return self.name

class Lead(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Dia que a Lead Chegou"))
    first_name = models.CharField(max_length=255, verbose_name=_("Nome da Lead"), blank=True)
    company_name = models.CharField(max_length=255, verbose_name=_("Empresa da Lead"), blank=True)
    responsible = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # opcional, depende se você quer forçar uma seleção
        verbose_name=_("Responsável pela Lead")
    )
    email = models.EmailField(max_length=255, unique=False, verbose_name=_("Email"), blank=True)
    instagram = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Instagram"))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    whatsapp = models.CharField(max_length=20, verbose_name=_("Whatsapp (Telefone)"), blank=True)
    first_contact_date = models.DateField(verbose_name=_("Data Primeiro Contato"),null=True, blank=True)
    return_contact = models.DateField(verbose_name=_("Retornar Contato Em"),null=True, blank=True)
    origin = models.ForeignKey(Origin, on_delete=models.SET_NULL, null=True, verbose_name="Origem da Lead")
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, verbose_name=_("Tipos de Serviço da Lead"))
    # Continuação dos outros campos
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, verbose_name="Prioridade")
    city = models.CharField(max_length=50, verbose_name=_("Cidade"), blank=True)
    state = models.CharField(max_length=2, verbose_name=_("Estado"), blank=True)

    lead_info = models.TextField(max_length=2500, blank=True, verbose_name=_("Informações Sobre a Lead"))

    def __str__(self):
        return '%s %s' % (self.first_name, self.company_name)
    
class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, verbose_name=_("Lead associada"))
    actual_date = models.DateField(blank=True, null=True, verbose_name=_("Data Realizada do Contato"))
    planned_date = models.DateField(verbose_name=_("Data do Próximo Contato"))
    notes = models.TextField(max_length=50, blank=True, verbose_name=_("Anotações"))

    def __str__(self):
        return f"Follow-up for {self.lead.first_name} on {self.planned_date}"

