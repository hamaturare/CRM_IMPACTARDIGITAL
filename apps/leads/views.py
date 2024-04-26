from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead

class LeadsView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/leads.html'
    context_object_name = 'leads'
    paginate_by = 50  # Shows 50 leads per page
    login_url = reverse_lazy('home')
