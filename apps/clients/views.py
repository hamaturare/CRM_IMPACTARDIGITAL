from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Client
from django.views.generic import UpdateView
from django.shortcuts import redirect, render
from django.views.generic import DeleteView
from django.db.models import Q
from .forms import ClientForm
from django.views import View
from django.contrib import messages
from django.forms import DateInput


class ClientsView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/clients.html'
    paginate_by = 50  # Shows 50 clients per page
    login_url = reverse_lazy('home')

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
    success_url = reverse_lazy('clients')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # get the form
        # Certifique-se de que os campos existem antes de atribuir widgets
        if 'contract_date' in form.fields:
            form.fields['contract_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'next_contact_date' in form.fields:
            form.fields['next_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        return form
    
    def post(self, request, *args, **kwargs):
        # Adiciona a mensagem antes de processar o formulário
        messages.success(self.request, 'Cliente atualizado com sucesso!!!')
        return super().post(request, *args, **kwargs)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients')
    
    def delete(self, request, *args, **kwargs):
        messages.error(self.request, 'Cliente deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class AddClientView(LoginRequiredMixin, View):
    template_name = 'clients/add_client.html'

    def get(self, request, *args, **kwargs):
        form = ClientForm()
        self.setup_date_widgets(form)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ClientForm(request.POST)
        self.setup_date_widgets(form)
        # Adiciona a mensagem de sucesso antes de verificar se o formulário é válido
        messages.success(self.request, 'Cliente adicionado com sucesso!!!')
        if form.is_valid():
            form.save()
            return redirect('clients')  # Redireciona após o cadastro ser bem-sucedido
        return render(request, self.template_name, {'form': form})

    def setup_date_widgets(self, form):
        # Configura os widgets de data somente se os campos existirem
        if 'contract_date' in form.fields:
            form.fields['contract_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'next_contact_date' in form.fields:
            form.fields['next_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
    