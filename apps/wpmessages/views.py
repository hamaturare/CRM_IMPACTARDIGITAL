from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WpMessages
from django.views.generic import UpdateView
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView
from django.db.models import Q
from django.views import View
from django.contrib import messages
from django.forms import DateInput
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .functions import send_whatsapp_message

class WpMessagesView(LoginRequiredMixin, ListView):
    model = WpMessages
    template_name = 'wpmessages/wpmessages.html'
    login_url = reverse_lazy('home')

class WhatsAppWebhookView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        VERIFY_TOKEN = settings.WHATSAPP_VERIFY_TOKEN
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return HttpResponse(challenge, status=200)
            else:
                return HttpResponse('Forbidden', status=403)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        if 'object' in data and 'entry' in data:
            if data['object'] == 'whatsapp_business_account':
                try:
                    for entry in data['entry']:
                        phoneNumber = entry['changes'][0]['value']['metadata']['display_phone_number']
                        phoneId = entry['changes'][0]['value']['metadata']['phone_number_id']
                        profileName = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        whatsAppId = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        fromId = entry['changes'][0]['value']['messages'][0]['from']
                        messageId = entry['changes'][0]['value']['messages'][0]['id']
                        timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        # Send a response message
                        phoneNumber = "5527999371909"
                        message = 'RE: {} was received.'.format(text)
                        send_whatsapp_message(phoneNumber, message)

                except Exception as e:
                    print(f"Error processing WhatsApp message: {e}")
                    return HttpResponse('error', status=500)

        return HttpResponse('success', status=200)
