from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, FollowUp
from django.views.generic import UpdateView
from django.shortcuts import redirect, render
from django.views.generic import DeleteView, DetailView
from django.db.models import Q
from .forms import LeadForm, FollowUpForm
from django.views import View
from django.contrib import messages
from django.forms import DateInput


class LeadsView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/leads.html'
    context_object_name = 'leads'
    paginate_by = 50  # Shows 50 leads per page
    login_url = reverse_lazy('home')

    def get_queryset(self):
        """Allow custom sorting and searching with safety checks."""
        queryset = Lead.objects.all()
        
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
        valid_sort_fields = ['first_name', 'company_name', 'email', 'created_at', 'id', 'service_type']
        
        # Obtendo o campo de ordenação da query string e verificando se é válida
        ordering = self.request.GET.get('sort', 'first_name')
        if ordering in valid_sort_fields:
            return queryset.order_by(ordering)
        
        return queryset.order_by('first_name')


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/update_lead.html'
    success_url = reverse_lazy('leads')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # get the form
        # Certifique-se de que os campos existem antes de atribuir widgets
        if 'first_contact_date' in form.fields:
            form.fields['first_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'return_contact' in form.fields:
            form.fields['return_contact'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        return form
    
    def post(self, request, *args, **kwargs):
        # Adiciona a mensagem antes de processar o formulário
        messages.success(self.request, 'Lead atualizado com sucesso!!!')
        return super().post(request, *args, **kwargs)


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads')
    
    def delete(self, request, *args, **kwargs):
        messages.error(self.request, 'Lead deletado com sucesso!')
        return super().delete(request, *args, **kwargs)


class AddLeadView(LoginRequiredMixin, View):
    template_name = 'leads/add_lead.html'

    def get(self, request, *args, **kwargs):
        form = LeadForm()
        self.setup_date_widgets(form)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LeadForm(request.POST)
        self.setup_date_widgets(form)
        # Adiciona a mensagem de sucesso antes de verificar se o formulário é válido
        messages.success(self.request, 'Lead adicionado com sucesso!!!')
        if form.is_valid():
            form.save()
            return redirect('leads')  # Redireciona após o cadastro ser bem-sucedido
        return render(request, self.template_name, {'form': form})

    def setup_date_widgets(self, form):
        # Configura os widgets de data somente se os campos existirem
        if 'first_contact_date' in form.fields:
            form.fields['first_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        if 'return_contact' in form.fields:
            form.fields['return_contact'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'leads/lead_info.html'
    context_object_name = 'lead'
    login_url = reverse_lazy('home')  # Garante que o usuário esteja logado
    success_url = reverse_lazy('leads')   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followup_form = FollowUpForm()
        # Configura os widgets dos campos de data
        followup_form.fields['planned_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        followup_form.fields['actual_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        context['followup_form'] = followup_form
        context['followups'] = FollowUp.objects.filter(lead=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        form = FollowUpForm(request.POST)
        if form.is_valid():
            followup = form.save(commit=False)
            followup.lead = self.get_object()
            followup.save()
            messages.success(request, 'Acompanhamento adicionado com sucesso!')
            return redirect('lead_info', pk=self.get_object().pk)
        else:
            form.fields['planned_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
            form.fields['actual_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
            context = self.get_context_data()
            context['followup_form'] = form
            return render(request, self.template_name, context)