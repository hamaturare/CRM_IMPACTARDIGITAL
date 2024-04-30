from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead
from django.views.generic import UpdateView
from django import forms
from django.shortcuts import redirect, render
from django.views.generic import DeleteView
from django.db.models import Q
from .forms import LeadForm
from django.views import View


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
                Q(last_name__icontains=search_term) |
                Q(email__icontains=search_term) |
                Q(id__iexact=search_term) |
                Q(service_type__name__icontains=search_term)  # Filtro pelos nomes de objetivo dos serviços associados
            )

        # Lista dos campos válidos para ordenação
        valid_sort_fields = ['first_name', 'last_name', 'email', 'created_at', 'id', 'Objective', 'service_type']
        
        # Obtendo o campo de ordenação da query string e verificando se é válida
        ordering = self.request.GET.get('sort', 'first_name')
        if ordering in valid_sort_fields:
            return queryset.order_by(ordering)
        
        return queryset.order_by('first_name')


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    fields = ['first_name', 'last_name', 'email', 'instagram', 'website', 'whatsapp', 'first_contact_date', 'service_type', 'priority']  # Or use a form_class if you have a custom form
    template_name = 'leads/update_lead.html'
    success_url = reverse_lazy('leads')  # Assuming you have a named URL for listing leads

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['first_contact_date'].widget = forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
        return form
    
    """
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'delete' in request.POST:
            return redirect('delete_lead', pk=self.object.pk)
        elif 'back' in request.POST:
            return redirect('leads')
        return super(LeadUpdateView, self).post(request, *args, **kwargs)
    """    
    
    
# Sua nova view LeadDeleteView
class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads')


class AddLeadView(LoginRequiredMixin, View):
    form_class = LeadForm
    template_name = 'leads/add_lead.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lead')  # Redireciona após o cadastro ser bem-sucedido
        return render(request, self.template_name, {'form': form})