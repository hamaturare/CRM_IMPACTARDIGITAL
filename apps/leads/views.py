from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
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
        """Allow custom sorting and searching with safety checks. Also fetching the FollowUp database to be used in leads.html"""
        queryset = Lead.objects.all().prefetch_related('followup_set')
        
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
            if ordering == 'created_at':
                return queryset.order_by('-created_at')
            return queryset.order_by(ordering)
        
        return queryset.order_by('first_name')
    
class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/update_lead.html'

    def get_success_url(self):
        return reverse_lazy('lead_info', kwargs={'pk':self.object.pk})  

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

class FollowUpDeleteView(LoginRequiredMixin, DeleteView):
    model = FollowUp
    template_name = 'leads/confirm_delete_followup.html'

    def get_success_url(self):
        lead_id = self.object.lead.id
        return reverse_lazy('lead_info', kwargs={'pk': lead_id})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Follow-up deleted successfully!')
        return super().delete(request, *args, **kwargs)

class AddLeadView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'leads/add_lead.html'
    success_url = reverse_lazy('leads')
    
    def form_valid(self, form):
        messages.success(self.request, 'Lead adicionado com sucesso!!!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao adicionar a lead. Verifique os dados e tente novamente.')

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
        followup_form.fields['last_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        followup_form.fields['return_contact'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
        context['followup_form'] = followup_form
        context['followups'] = FollowUp.objects.all() #Include all follow-ups in the context and filter them in the template if needed.
        #context['followups'] = FollowUp.objects.filter(lead=self.get_object())
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
            form.fields['last_contact_date'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
            form.fields['return_contact'].widget = DateInput(attrs={'type': 'date', 'class': 'datepicker'})
            context = self.get_context_data()
            context['followup_form'] = form
            return render(request, self.template_name, context)