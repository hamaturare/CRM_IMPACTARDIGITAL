from django.conf import settings
from django.utils import timezone
from apps.visualadmin.models import ChatbotState, ChatbotQuestion, ChatbotOption
from apps.wpmessages.models import WpMessage
from datetime import datetime
import requests
import logging

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

def handle_incoming_message(
    lead_phone_number,
    profile_name,
    whatsapp_id,
    business_phone_number,
    message_id,
    text):

    try:
        # Trying to check if this phone number exists in database or not
        wp_message = WpMessage.objects.get(lead_phone_number=lead_phone_number)

        # Fetch the current state from ChatbotState
        current_state = wp_message.state

        if current_state:
            # Get the question associated with the current state
            question = current_state.questions.first()

            if question:
                # Find the option based on the user's response
                option = question.options.filter(option_text=text).first()

                if option:
                    # Update chat history and state
                    wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {option.response_message}"
                    wp_message.message_timestamp = timezone.now()

                    if option.next_state:
                        wp_message.state = option.next_state
                    else:
                        wp_message.state = None  # Mark as no more state

                    wp_message.save()
                    send_whatsapp_message(lead_phone_number, option.response_message)
                else:
                    # Handle invalid response
                    response_message = question.invalid_response_message or "Resposta inválida, tente novamente."
                    wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {response_message}"
                    wp_message.message_timestamp = timezone.now()
                    wp_message.save()
                    send_whatsapp_message(lead_phone_number, response_message)
            else:
                # Handle the case where there is no question for the state
                response_message = "Não há mais perguntas no momento."
                wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {response_message}"
                wp_message.message_timestamp = timezone.now()
                wp_message.state = None  # Mark as no more state
                wp_message.save()
                send_whatsapp_message(lead_phone_number, response_message)
        else:
            # Handle the case where state is None
            response_message = "Bem-vindo! Como posso ajudar?"
            wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {response_message}"
            wp_message.message_timestamp = timezone.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, response_message)

    except WpMessage.DoesNotExist:
        # Create a new WpMessage for the first contact
        initial_state = ChatbotState.objects.order_by('id').first()  # Get the first state created by admin

        wp_message = WpMessage.objects.create(
            lead_phone_number=lead_phone_number,
            profile_name=profile_name,
            message_text=text,
            chat_history=text,
            business_phone_number=business_phone_number,
            whatsapp_id=whatsapp_id,
            message_id=message_id,
            state=initial_state
        )

        first_question = initial_state.questions.first()
        if first_question:
            wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {first_question.question_text}"
            wp_message.message_timestamp = timezone.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, first_question.question_text)
        else:
            response_message = "Bem-vindo! Como posso ajudar?"
            wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {response_message}"
            wp_message.message_timestamp = timezone.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, response_message)
"""
#The function below is working but the messages are enbeded in the code what is not ideal.
def handle_incoming_message(
                            lead_phone_number,
                            profile_name,
                            whatsapp_id,
                            business_phone_number,
                            message_id,
                            text):
    try:
        #trying to check if this phone number exists in database or not
        wp_message = WpMessage.objects.get(lead_phone_number=lead_phone_number)

        # since the wp message is created and chechk above I need to check if the state inside WpMessage is = to initial
        if wp_message.state == WpMessage.STATE_AWAITING_SERVICE:
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
                wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {message}"
                wp_message.message_timestamp = datetime.now()
                wp_message.save()
                send_whatsapp_message(lead_phone_number, message)

            message += (
                "\nDeseja falar com um atendente pelo WhatsApp ou prefere que alguém entre em contato por telefone? 🤩 \n"
                "Digite o número abaixo: 👇👇\n\n"
                "1 - Desejo falar com um atendente pelo WhatsApp\n"
                "2 - Prefiro que alguém entre em contato por telefone"
            )

            wp_message.state = WpMessage.STATE_AWAITING_CONTACT_METHOD
            wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {message}"
            wp_message.message_timestamp = datetime.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, message)

        elif wp_message.state == WpMessage.STATE_AWAITING_CONTACT_METHOD:
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
                
                wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {message}"
                wp_message.message_timestamp = datetime.now()
                wp_message.save()
                send_whatsapp_message(lead_phone_number, message)

            wp_message.state = WpMessage.STATE_COMPLETED
            wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {message}"
            wp_message.message_timestamp = datetime.now()
            wp_message.save()
            send_whatsapp_message(lead_phone_number, message)

        elif wp_message.state == WpMessage.STATE_INITIAL:
            
            message = ("Olá, tudo bem? Em qual serviço você está interessado?\n"
                    "Digite o número abaixo:\n"
                    "1- Anúncios com Tráfego Pago\n "
                    "2- Sites e Landpages\n"
                    "3- Treinamento Presencial de Tráfego Pago\n"
                    "4- Outros Assuntos"
                    )
        
            wp_message.state = WpMessage.STATE_AWAITING_SERVICE
            wp_message.message_timestamp = datetime.now()
            wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {message}"
            wp_message.save()
            send_whatsapp_message(lead_phone_number, message)

    except:
        
        wp_message = WpMessage.objects.create(
            lead_phone_number=lead_phone_number,
            profile_name=profile_name,
            message_text=text,
            chat_history=text,
            business_phone_number=business_phone_number,
            whatsapp_id=whatsapp_id,
            message_id=message_id)

        message = ("Olá, tudo bem? Em qual serviço você está interessado?\n"
                    "Digite o número abaixo:\n"
                    "1- Anúncios com Tráfego Pago\n "
                    "2- Sites e Landpages\n"
                    "3- Treinamento Presencial de Tráfego Pago\n"
                    "4- Outros Assuntos"
                    )
        
        wp_message.state = WpMessage.STATE_AWAITING_SERVICE
        wp_message.message_timestamp = datetime.now()
        wp_message.chat_history += f"\n{profile_name}: {text}\nBot: {message}"
        wp_message.save()
        send_whatsapp_message(lead_phone_number, message)
"""