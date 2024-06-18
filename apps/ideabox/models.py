from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Priority(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Prioridade"))

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("Status"), default='Pending')

    def __str__(self):
        return self.name

class Suggestion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Usuário")
    title = models.TextField(max_length=50, verbose_name="Conteúdo", default="Título não especificado")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    priority = models.ForeignKey(Priority, on_delete=models.PROTECT , verbose_name="Prioridade")
    content = models.TextField(verbose_name="Conteúdo", blank=False)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name="Status", default=1)

    def __str__(self):
        return f"Suggestion by {self.user.username}"
