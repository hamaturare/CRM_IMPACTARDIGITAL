from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.

class ClientsView(LoginRequiredMixin, TemplateView):
    template_name = 'clients/clients.html'
    login_url = reverse_lazy('home')