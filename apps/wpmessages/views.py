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

# Create your views here.

class WpMessagesView(ListView,LoginRequiredMixin):
    model = WpMessages
    template_name = 'wpmessages/wpmessages.html'
    #context_object_name = 'wpmessages'
    #paginate_by = 50  # Shows 50 leads per page
    login_url = reverse_lazy('home')
    

    