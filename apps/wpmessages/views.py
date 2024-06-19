from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WpMessage
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST 
from django.conf import settings
from .functions import *
import json
import logging
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic.edit import DeleteView
from apps.leads.models import Lead, Origin, Priority, ServiceType

logger = logging.getLogger(__name__)

class WpMessagesView(LoginRequiredMixin, ListView):
    model = WpMessage
    template_name = 'wpmessages/wpmessages.html'
    context_object_name = 'wpmessages'
    paginate_by = 50  # Shows 50 leads per page
    login_url = reverse_lazy('home')

    def get_queryset(self):
        """Allow custom sorting and searching with safety checks. Also fetching the FollowUp database to be used in leads.html"""
        queryset = WpMessage.objects.all()
        
        # Adicionando funcionalidade de busca
        search_term = self.request.GET.get('search_term', '').strip()
        if search_term:
            queryset = queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(company_name__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(id__iexact=search_term) |
                Q(service_type__name__icontains=search_term)  # Filtro pelos nomes de objetivo dos serviços associados
            )

        # Lista dos campos válidos para ordenação
        valid_sort_fields = ['profile_name', 'lead_phone_number', 'created_at', 'contact_method', 'state', 'service_interest']
        
        # Obtendo o campo de ordenação da query string e verificando se é válida
        ordering = self.request.GET.get('sort', 'profile_name')
        if ordering in valid_sort_fields:
            return queryset.order_by(ordering)
        
        return queryset.order_by('profile_name')
    
    def get_context_data(self, **kwargs):
        """Add extra context including message count."""
        context = super().get_context_data(**kwargs)
        context['message_count'] = WpMessage.objects.count()  # Get the total number of messages
        return context
    
class DeleteWpMessageView(LoginRequiredMixin, DeleteView):
    model = WpMessage
    success_url = reverse_lazy('wpmessages')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Lead deletada com sucesso.')
        return super().delete(request, *args, **kwargs)
    
class MigrateToLeadView(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):
        wpmessage = get_object_or_404(WpMessage, pk=self.kwargs['pk'])

        # Criar nova lead com os dados do wpmessage
        lead = Lead.objects.create(
            first_name=wpmessage.profile_name,
            whatsapp=wpmessage.lead_phone_number,
            lead_info=wpmessage.chat_history,
            #service_type=ServiceType.objects.filter(name=wpmessage.service_interest).first(),
            # Adicione mais campos conforme necessário
        )

        wpmessage.delete()
        
        messages.success(request, 'Lead migrada com sucesso.')
        return redirect('leads') #testar

@csrf_protect
@require_POST
def update_contacted_status(request, wpmessage_id):
    try:
        wpmessage = WpMessage.objects.get(id=wpmessage_id)
        contacted = 'contacted' in request.POST
        wpmessage.contacted = contacted
        wpmessage.save()
        return redirect('wpmessages')
    except WpMessage.DoesNotExist:
        return HttpResponse('WpMessage not found', status=404)

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
                        #phone_id = entry['changes'][0]['value']['metadata']['phone_number_id']
                        profile_name = entry['changes'][0]['value']['contacts'][0]['profile']['name']
                        whatsapp_id = entry['changes'][0]['value']['contacts'][0]['wa_id']
                        lead_phone_number = entry['changes'][0]['value']['messages'][0]['from'] # Number to respond to. This is the Lead phone Number that enters in contact
                        message_id = entry['changes'][0]['value']['messages'][0]['id']
                        #timestamp = entry['changes'][0]['value']['messages'][0]['timestamp']
                        text = entry['changes'][0]['value']['messages'][0]['text']['body']

                        #Handle the incoming message
                        handle_incoming_message(
                            lead_phone_number,
                            profile_name,
                            whatsapp_id,
                            business_phone_number,
                            message_id,
                            text)

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