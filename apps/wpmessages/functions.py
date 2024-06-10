from django.conf import settings
from .models import WpMessage
import requests
import logging
from datetime import datetime
from .models import WpMessage


logger = logging.getLogger(__name__)

def send_whatsapp_message(phone_number, message):
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": phone_number,
        "type": "text",
        "text": {"body": message}
    }

    try:
        response = requests.post(settings.WHATSAPP_API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        return {"status": "error", "message": str(e)}

    return response.json()

def handle_incoming_message(lead_phone_number, profile_name, business_phone_number, text):

    try:
        #trying to check if this phone number exists in database or not
        wp_message = WpMessage.objects.get(lead_phone_number=lead_phone_number)

        # since the wp message is created and chechk above I need to check if the state inside WpMessage is = to initial
        if wp_message.state == 'awaiting_service':
            if text == '1':
                wp_message.service_interest = 'Anúncios com Tráfego Pago'
                message = "Obrigado pelo seu interesse em nossos serviço de Anúncios com Tráfego Pago. 🤩"
            elif text == '2':
                wp_message.service_interest = 'Sites e Landpages'
                message = "Obrigado pelo seu interesse em nossos serviço de criação de Sites e Landpages. 🤩"
            elif text == '3':
                wp_message.service_interest = 'Treinamento Presencial de Tráfego Pago'
                message = "Obrigado pelo seu interesse em em nossos serviço de Treinamento Presencial de Tráfego Pago. 🤩"
            elif text == '4':
                wp_message.service_interest = 'Outros Assuntos'
                message = "Obrigado pelo seu interesse em Outros Assuntos."
            else:
                message = (
                    "Desculpe, não entendi sua resposta. 🥺 \n Por favor, digite o número correspondente ao serviço de seu interesse:\n "
                    "1- Anúncios com Tráfego Pago\n"
                    "2- Sites e Landpages\n"
                    "3- Treinamento Presencial de Tráfego Pago\n"
                    "4- Outros Assuntos"
                )
                wp_message.chat_history += f"\nUser: {text}\nBot: {message}"
                wp_message.message_timestamp = datetime.now()
                wp_message.save()
                send_whatsapp_message(lead_phone_number, message)

            message += (
                "\nDeseja falar com um atendente pelo WhatsApp ou prefere que alguém entre em contato por telefone? 🤩 \n"
                "Digite o número abaixo: 👇👇\n\n"
                "1 - Desejo falar com um atendente pelo WhatsApp\n"
                "2 - Prefiro que alguém entre em contato por telefone"
            )

            wp_message.state = 'awaiting_contact_method'
            wp_message.chat_history += f"\nUser: {text}\nBot: {message}"
            wp_message.message_timestamp = datetime.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, message)

        elif wp_message.state == 'awaiting_contact_method':
            if text == '1':
                wp_message.contact_method = 'WhatsApp'
                message = "Obrigado! Um de nossos atendentes entrará em contato com você pelo WhatsApp em breve. 🤩"
            elif text == '2':
                wp_message.contact_method = 'Telefone'
                message = "Obrigado! Um de nossos atendentes entrará em contato com você por telefone em breve. 🤩 "
            else:
                message = (
                    "Desculpe, não entendi sua resposta. Por favor, digite o número correspondente à sua preferência:\n"
                    "1 - Desejo falar com um atendente pelo WhatsApp\n"
                    "2 - Prefiro que alguém entre em contato por telefone"
                )
                
                wp_message.chat_history += f"\nUser: {text}\nBot: {message}"
                wp_message.message_timestamp = datetime.now()
                wp_message.save()
                send_whatsapp_message(lead_phone_number, message)

            wp_message.state = 'completed'
            wp_message.chat_history += f"\nUser: {text}\nBot: {message}"
            wp_message.message_timestamp = datetime.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, message)

        elif wp_message.state == 'completed':

            message = "Obrigado por usar o chatbot da ID. O Teste funcionou perfeitamente. Para tentar mais uma vez digite qualquer coisa\n\n Obrigado!!! \n 😍"
            wp_message.state = 'initial'
            wp_message.chat_history += f"\nUser: {text}\nBot: {message}"
            wp_message.message_timestamp = datetime.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, message)
            #mandar algum aviso no CRM ou email etc... Lead quente tentando falar novamente.

        elif wp_message.state == 'initial':
            
            message = ("Olá, tudo bem? Em qual serviço você está interessado?\n"
                    "Digite o número abaixo:\n"
                    "1- Anúncios com Tráfego Pago\n "
                    "2- Sites e Landpages\n"
                    "3- Treinamento Presencial de Tráfego Pago\n"
                    "4- Outros Assuntos"
                    )
        
            wp_message.state = 'awaiting_service'
            wp_message.message_timestamp = datetime.now()
            wp_message.chat_history += f"\nUser: {text}\nBot: {message}"
            wp_message.save()
            send_whatsapp_message(lead_phone_number, message)

    except:
        
        wp_message = WpMessage.objects.create(
            lead_phone_number=lead_phone_number,
            profile_name=profile_name,
            message_text=text,
            chat_history=text,
            business_phone_number=business_phone_number)

        message = ("Olá, tudo bem? Em qual serviço você está interessado?\n"
                    "Digite o número abaixo:\n"
                    "1- Anúncios com Tráfego Pago\n "
                    "2- Sites e Landpages\n"
                    "3- Treinamento Presencial de Tráfego Pago\n"
                    "4- Outros Assuntos"
                    )
        
        wp_message.state = 'awaiting_service'
        wp_message.message_timestamp = datetime.now()
        wp_message.chat_history += f"\nUser: {text}\nBot: {message}"
        wp_message.save()
        send_whatsapp_message(lead_phone_number, message)