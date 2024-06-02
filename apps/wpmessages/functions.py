from django.conf import settings
from .models import WpMessage
import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def send_whatsapp_message(phone_number, message):
    url = f"{settings.WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_ID}/messages"
    headers = {"Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return {"status": "error", "message": str(e)}

    return response.json()

def handle_incoming_message(business_phone_number, phone_id, profile_name, whatsapp_id, lead_phone_number, message_id, timestamp, text):
    wp_message, created = WpMessage.objects.get_or_create(
        lead_phone_number=lead_phone_number,
        defaults={
            'phone_id': phone_id,
            'profile_name': profile_name,
            'whatsapp_id': whatsapp_id,
            'message_id': message_id,
            'timestamp': datetime.fromtimestamp(int(timestamp)),
            'message_text': text,
            'business_phone_number': business_phone_number,
            'chat_history': text,  # Initialize chat history with the first message
            'state': 'initial',
            'thanked': False
        }
    )

    if not created:
        wp_message.chat_history += f"\n{text}"
        wp_message.save()

    if wp_message.state == 'initial':
        response_message = (
            "Olá, tudo bem? Em qual serviço você está interessado?\n"
            "Digite o número abaixo:\n"
            "1- Anúncios com Tráfego Pago\n"
            "2- Sites e Landpages\n"
            "3- Treinamento Presencial de Tráfego Pago\n"
            "4- Outros Assuntos"
        )
        wp_message.state = 'awaiting_service'
    elif wp_message.state == 'awaiting_service':
        if text == '1':
            wp_message.service_interest = 'Anúncios com Tráfego Pago'
            response_message = "Obrigado pelo seu interesse em Anúncios com Tráfego Pago."
        elif text == '2':
            wp_message.service_interest = 'Sites e Landpages'
            response_message = "Obrigado pelo seu interesse em Sites e Landpages."
        elif text == '3':
            wp_message.service_interest = 'Treinamento Presencial de Tráfego Pago'
            response_message = "Obrigado pelo seu interesse em Treinamento Presencial de Tráfego Pago."
        elif text == '4':
            wp_message.service_interest = 'Outros Assuntos'
            response_message = "Obrigado pelo seu interesse em Outros Assuntos."
        else:
            response_message = (
                "Desculpe, não entendi sua resposta. Por favor, digite o número correspondente ao serviço de seu interesse:\n"
                "1- Anúncios com Tráfego Pago\n"
                "2- Sites e Landpages\n"
                "3- Treinamento Presencial de Tráfego Pago\n"
                "4- Outros Assuntos"
            )
            send_whatsapp_message(lead_phone_number, response_message)
            wp_message.save()
            return

        response_message += (
            "\nDeseja falar com um atendente pelo WhatsApp ou prefere que alguém entre em contato por telefone?\n"
            "Digite o número abaixo:\n"
            "1 - Desejo falar com um atendente pelo WhatsApp\n"
            "2 - Prefiro que alguém entre em contato por telefone"
        )
        wp_message.state = 'awaiting_contact_method'
    elif wp_message.state == 'awaiting_contact_method':
        if text == '1':
            wp_message.contact_method = 'WhatsApp'
            response_message = "Obrigado! Um de nossos atendentes entrará em contato com você pelo WhatsApp em breve."
        elif text == '2':
            wp_message.contact_method = 'Telefone'
            response_message = "Obrigado! Um de nossos atendentes entrará em contato com você por telefone em breve."
        else:
            response_message = (
                "Desculpe, não entendi sua resposta. Por favor, digite o número correspondente à sua preferência:\n"
                "1 - Desejo falar com um atendente pelo WhatsApp\n"
                "2 - Prefiro que alguém entre em contato por telefone"
            )
            send_whatsapp_message(lead_phone_number, response_message)
            wp_message.save()
            return

        wp_message.state = 'completed'
    
    if wp_message.state == 'completed' and not wp_message.thanked:
        response_message = "Obrigado por entrar em contato conosco. Um de nossos atendentes estará com você em breve."
        wp_message.thanked = True
    elif wp_message.state == 'completed' and wp_message.thanked:
        return  # Do not send any message if already thanked

    wp_message.chat_history += f"\nUser: {text}\nBot: {response_message}"
    wp_message.save()
    send_whatsapp_message(lead_phone_number, response_message)
