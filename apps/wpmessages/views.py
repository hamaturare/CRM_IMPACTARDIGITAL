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
from django.views import View

# Create your views here.

class WpMessagesView(ListView, LoginRequiredMixin):
    model = WpMessages
    template_name = 'wpmessages/wpmessages.html'
    #context_object_name = 'wpmessages'
    #paginate_by = 50  # Shows 50 leads per page
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
        # Processar os dados recebidos
        print('Received webhook:', data)  # Ou registre isso em um arquivo de log
        return JsonResponse({"status": "success"})
    

    