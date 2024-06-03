from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WpMessage
from django.views.generic import UpdateView
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView
from django.db.models import Q
from django.views import View
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .functions import *
import json
import logging

logger = logging.getLogger(__name__)

class WpMessagesView(LoginRequiredMixin, ListView):
    model = WpMessage
    template_name = 'wpmessages/wpmessages.html'
    login_url = reverse_lazy('home')

@csrf_exempt
def whatsapp_webhook(request):
    #logger.info('Webhook accessed')
    if request.method == 'GET':
        try:
            VERIFY_TOKEN = 'e4679551-2c1e-420a-92a0-40d965a8a66f'
            mode = request.GET.get('hub.mode')
            token = request.GET.get('hub.verify_token')
            challenge = request.GET.get('hub.challenge')

            #logger.info(f'Mode: {mode}, Token: {token}, Challenge: {challenge}')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return HttpResponse(challenge, status=200)
            else:
                logger.warning('Forbidden access attempted with token: %s', token)
                return HttpResponse('Forbidden', status=403)
        except Exception as e:
            logger.error(f'Error in GET request: {e}')
            return HttpResponse('Internal Server Error', status=500)

    if request.method == 'POST':
        data = json.loads(request.body)
        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        business_phone_number= entry['changes'][0]['value']['metadata']['display_phone_number'] # This is our number from whatsapp business
                        phone_id = entry['changes'][0]['value']['metadata']['phone_number_id']
                        profile_name = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        whatsapp_id = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        lead_phone_number = entry['changes'][0]['value']['messages'][0]['from'] # Number to respond to. This is the Lead phone Number that enters in contact
                        message_id = entry['changes'][0]['value']['messages'][0]['id']
                        timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        #Handle the incoming message
                        handle_incoming_message(
                            lead_phone_number,
                            #profile_name,
                            #phone_id,
                            #whatsapp_id,
                            #usiness_phone_number,
                            #essage_id,
                            #timestamp,
                            text)


                        """
                        lead_phone_number = "5527999371909"
                        message = 'RE: {} was received'.format(text)
                        send_whatsapp_message(lead_phone_number, message)
                        """
                except:
                    pass
        return HttpResponse('success', status=200)


"""
class WhatsAppWebhookView():
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        VERIFY_TOKEN = 'e4679551-2c1e-420a-92a0-40d965a8a66f'
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return HttpResponse(challenge, status=200)
            else:
                return HttpResponse('Forbidden', status=403)
        return HttpResponse('Bad Request', status=400)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        lead_phone_number= entry['changes'][0]['value']['metadata']['display_phone_number'] # Send the Whatsapp to this is the Lead phone Number
                        #phone_id = entry['changes'][0]['value']['metadata']['phone_number_id']
                        profile_name = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        #whatsapp_id = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        #business_phone_number = entry['changes'][0]['value']['messages'][0]['from']
                        #message_id = entry['changes'][0]['value']['messages'][0]['id']
                        #timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        # Handle the incoming message
                        #handle_incoming_message(
                         #   lead_phone_number,
                         #   profile_name,
                            #phone_id,
                            #whatsapp_id,
                            #usiness_phone_number,
                            #essage_id,
                            #timestamp,
                         #   text)
                        
                except Exception as e:
                    print(f"Error processing WhatsApp message: {e}")
                    return HttpResponse('error', status=500)
        return HttpResponse('success', status=200)
"""