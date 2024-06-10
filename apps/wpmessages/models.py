from django.db import models
from django.utils import timezone

class WpMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp da mensagem
    lead_phone_number = models.CharField(max_length=20, unique=True)  # Número de telefone da lead
    profile_name = models.CharField(max_length=100, blank=True, null=True)  # Nome do perfil da lead
    whatsapp_id = models.CharField(max_length=20, blank=True, null=True)  # ID do WhatsApp da lead
    message_id = models.CharField(max_length=50, blank=True, null=True)  # ID da mensagem
    message_timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)  # Timestamp da mensagem
    message_text = models.TextField()  # Texto da mensagem
    business_phone_number = models.CharField(max_length=15, blank=True, null=True)  # Número de telefone do negócio (Our number) que contactou a lead, que envia a mensagem
    phone_id = models.CharField(max_length=20, blank=True, null=True)  # ID do telefone do negócio (Our number)
    chat_history = models.TextField(blank=True, null=True)  # Histórico de chat

    state = models.CharField(max_length=50, default='Initial', blank=True, null=True)  # Status do chat
    contacted = models.BooleanField(default=False)  # Chat finalizado com obrigado
    service_interest = models.CharField(max_length=100, blank=True, null=True)  # Interesse no serviço
    contact_method = models.CharField(max_length=50, blank=True, null=True)  # Método de contato preferido

    def __str__(self):
        return self.lead_phone_number