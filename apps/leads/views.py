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

    def get_queryset(self):
        """Allow custom sorting with safety checks."""
        valid_sort_fields = ['first_name', 'last_name', 'email', 'created_at', 'id', 'Objective', 'service_type']  # Updated to include 'last_name'
        ordering = self.request.GET.get('sort', 'first_name')  # Default to 'first_name' if no sort parameter provided
        if ordering not in valid_sort_fields:
            ordering = 'first_name'
        return Lead.objects.all().order_by(ordering)
