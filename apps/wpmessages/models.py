from django.db import models

class WpMessage(models.Model):
    lead_phone_number = models.CharField(max_length=15) # Número de telefone da lead
    profile_name = models.CharField(max_length=100) # Nome do perfil da lead
    whatsapp_id = models.CharField(max_length=20) # ID do WhatsApp da lead
    message_id = models.CharField(max_length=50) # ID da mensagem
    timestamp = models.DateTimeField() # Timestamp da mensagem
    message_text = models.TextField() # Texto da mensagem
    business_phone_number = models.CharField(max_length=15) # Número de telefone do negócio (Our number) que contactou a lead, que envia a menssagem
    phone_id = models.CharField(max_length=20) # ID do telefone do negócio (Our number)
    chat_history = models.TextField() # Histórico de chat

    state = models.CharField(max_length=50, default='initial') # Status do chat
    thanked = models.BooleanField(default=False) # Chate finalizado com obrigado
    service_interest = models.CharField(max_length=100, blank=True, null=True) # Interesse no serviço
    contact_method = models.CharField(max_length=50, blank=True, null=True) # Método de contato preferido

    def __str__(self):
        return self.lead_phone_number
