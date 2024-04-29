from django.db import models
from django.utils.translation import gettext_lazy as _

class ServiceType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nome do Objetivo"))

    def __str__(self):
        return self.name

OBJECTIVE_CHOICES = (
    ('sales', _('Vendas')),
    ('support', _('Suporte')),
    ('feedback', _('Feedback')),
    ('other', _('Outro')),
    ('Teste', _('Teste'))
)

class Lead(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name=_("Dia que a Lead Chegou"))
    first_name = models.CharField(max_length=255, verbose_name=_("Nome da Lead"), blank=False)
    last_name = models.CharField(max_length=255, verbose_name=_("Sobrenome da Lead"), blank=False)
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Email"), blank=False)
    instagram = models.URLField(blank=True, null=True, verbose_name=_("Instagram"))
    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    whatsapp = models.CharField(max_length=20, verbose_name=_("Whatsapp (Telefone)"), blank=False)
    first_contact_date = models.DateField(verbose_name=_("Data Primeiro Contato"),null=True, blank=True)
    objective = models.CharField(
        max_length=100,
        verbose_name=_("Objetivo da Lead"),
        choices=OBJECTIVE_CHOICES,
        default='other'  # Opção padrão
    )
    service_type = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True, verbose_name=_("Tipos de Serviço da Lead"))
    # Continuação dos outros campos
    priority = models.IntegerField(verbose_name=_("Prioridade"))
    city = models.CharField(max_length=50, verbose_name=_("Cidade"), blank=True)
    state = models.CharField(max_length=2, verbose_name=_("Estado"), blank=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)
