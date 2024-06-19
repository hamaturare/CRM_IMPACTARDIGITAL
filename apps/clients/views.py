from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client, ClientLeads
from django.views.generic import UpdateView, DetailView, DeleteView
from django.shortcuts import redirect, render
from django.db.models import Q
from .forms import ClientForm, ClientLeadsForm
from django.views import View
from django.contrib import messages
from django.forms import DateInput
from apps.leads.models import Lead
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST 
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


@csrf_protect
@require_POST
def update_client_status_listview(request, pk):
    if request.method == 'POST':
        client = Client.objects.get(pk=pk)
        client.status = not client.status
        client.save()
        return redirect('clients')
    return HttpResponseNotAllowed(['POST'])

@csrf_protect
@require_POST
def update_client_status_client_info(request, pk):
    client = Client.objects.get(pk=pk)
    client.status = not client.status
    client.save()
    return JsonResponse({'status': client.status})

class ClientsView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/clients.html'
    paginate_by = 50  # Shows 50 clients per page
    login_url = reverse_lazy('home')
    context_object_name = 'clients'

    def get_queryset(self):
        """Allow custom sorting and searching with safety checks."""
        queryset = Client.objects.all()
        
        # Adicionando funcionalidade de busca
        search_term = self.request.GET.get('search_term', '').strip()
        if search_term:
            queryset = queryset.filter(
                Q(client_name__icontains=search_term) |
                Q(company_name__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(id__iexact=search_term) |
                Q(service_type__name__icontains=search_term)  # Filtro pelos nomes de objetivo dos serviços associados
            )

        # Lista dos campos válidos para ordenação
        valid_sort_fields = ['client_name', 'company_name', 'email', 'created_at', 'id', 'service_type']
        
        # Obtendo o campo de ordenação da query string e verificando se é válida
        ordering = self.request.GET.get('sort', 'client_name')
        if ordering in valid_sort_fields:
            return queryset.order_by(ordering)
        
        return queryset.order_by('client_name')
    
class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/update_client.html'
    
    def get_success_url(self):
        return reverse_lazy('client_info', kwargs={'pk':self.object.pk})
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # get the form
        # Certifique-se de que os campos existem antes de atribuir widgets
        if 'date_of_birth' in form.fields:
            form.fields['date_of_birth'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'contract_date' in form.fields:
            form.fields['contract_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'next_contact_date' in form.fields:
            form.fields['next_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        return form
    
    def post(self, request, *args, **kwargs):
        # Adiciona a mensagem antes de processar o formulário
        messages.success(self.request, 'Cliente atualizado com sucesso!!!')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_url'] = self.request.session.get('prev_url', reverse_lazy('clients'))
        return context

class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients')
    
    def delete(self, request, *args, **kwargs):
        messages.error(self.request, 'Cliente deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class AddClientView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'clients/add_client.html'
    success_url = reverse_lazy('clients')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Configura os widgets de data somente se os campos existirem
        if 'contract_date' in form.fields:
            form.fields['contract_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'date_of_birth' in form.fields:
            form.fields['date_of_birth'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'next_contact_date' in form.fields:
            form.fields['next_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Cliente adicionado com sucesso!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao adicionar o cliente. Verifique os dados e tente novamente.')
        return super().form_invalid(form)

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'clients/client_info.html'
    context_object_name = 'client'
    login_url = reverse_lazy('home')  # Garante que o usuário esteja logado
    success_url = reverse_lazy('clients')       
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_leads_form = ClientLeadsForm()
        # Configura os widgets dos campos de data
        context['client_leads_form'] = client_leads_form
        context['client_leads'] = ClientLeads.objects.filter(client=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        form = ClientLeadsForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.client = self.get_object()
            followup.save()
            messages.success(request, 'Indicação adicionada com sucesso!')
            return redirect('client_info', pk=self.get_object().pk)
        
class MigrateClientLeadView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        client_lead = get_object_or_404(ClientLeads, pk=self.kwargs['pk'])

        # Creating a new Lead object with fields from ClientLeads
        lead = Lead.objects.create(
            first_name=client_lead.name,
            whatsapp=client_lead.whatsapp,
            email=client_lead.email,
            lead_info=client_lead.notes,
            company_name=client_lead.company_name,  # if company_name is required
            # Add more fields as necessary
        )

        # Deleting the client_lead after migration
        client_lead.delete()

        messages.success(request, 'Lead migrada com sucesso.')
        return redirect('leads')