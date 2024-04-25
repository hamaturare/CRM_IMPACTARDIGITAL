from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Lead

# Create your views here.

class LeadsView(LoginRequiredMixin, TemplateView):
    template_name = 'leads/leads.html'
    login_url = reverse_lazy('home')
    

def leads(request):
    leads = Lead.objects.all()
    
    return render(request, 'leads/leads.html', {'leads':leads })