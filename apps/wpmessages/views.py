from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WpMessage
from django.views.generic import UpdateView
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView
from django.db.models import Q
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .functions import handle_incoming_message
import json

class WpMessagesView(LoginRequiredMixin, ListView):
    model = WpMessage
    template_name = 'wpmessages/wpmessages.html'
    login_url = reverse_lazy('home')

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        VERIFY_TOKEN = 'e4679551-2c1e-420a-92a0-40d965a8a66f'
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('Forbidden', status=403)

    elif request.method == 'POST':
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
                        handle_incoming_message(
                            lead_phone_number,
                            #profile_name,
                            #phone_id,
                            #whatsapp_id,
                            #usiness_phone_number,
                            #essage_id,
                            #timestamp,
                            text)
                        
                except Exception as e:
                    print(f"Error processing WhatsApp message: {e}")
                    return HttpResponse('error', status=500)
        return HttpResponse('success', status=200)
