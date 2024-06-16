from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SuggestionForm, SuggestionUpdateForm
from .models import Suggestion
from django.db.models import Q
from django.contrib import messages
from django.views.generic import UpdateView, DetailView
from django.http import Http404
from django.views.generic import DeleteView
from django.core.mail import send_mail
from django.conf import settings
import logging
import threading

# Set up logging
logger = logging.getLogger(__name__)

def send_email_async(recipient_list, subject, message):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email sent to {recipient_list}")
    except Exception as e:
        logger.error(f"Failed to send email to {recipient_list}: {e}")

class SuggestionsListView(LoginRequiredMixin, ListView):
    model = Suggestion
    context_object_name = 'suggestions'
    template_name = 'ideabox/suggestions_list.html'
    paginate_by = 50 

    def get_queryset(self):
        queryset = super().get_queryset()  # Inicia com um queryset padrão
        search_term = self.request.GET.get('search_term', '').strip()

        if search_term:
            queryset = queryset.filter(
                Q(user__username__icontains=search_term) |
                Q(title__icontains=search_term) |
                Q(content__icontains=search_term) |
                Q(priority__name__icontains=search_term)
            )

        ordering = self.request.GET.get('sort', 'created_at')
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

class SubmitSuggestionView(LoginRequiredMixin, CreateView):
    model = Suggestion
    form_class = SuggestionForm
    template_name = 'ideabox/submit_suggestion.html'
    success_url = reverse_lazy('suggestions_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Sugestão Enviada Com Sucesso')
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        admin_emails = settings.EMAIL_ADMINS
        user_email = self.request.user.email
        recipient_list = admin_emails + [user_email]
        subject = 'Nova Sugestão Recebida'
        message = 'Uma nova sugestão foi submetida por {}. \n\nTítulo: {}\n\nSugestão: {}\n\nImplementaremos o mais Rápido possível\n\n Att,\n\n Admin 😎'.format(
            self.request.user.username,
            form.instance.title,
            form.instance.content
        )

        threading.Thread(target=send_email_async, args=(recipient_list, subject, message)).start()
        return response

class SuggestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Suggestion
    form_class = SuggestionUpdateForm
    template_name = 'ideabox/view_suggestion.html'
    success_url = reverse_lazy('suggestions_list')

    def form_valid(self, form):
        original_status = self.get_object().status
        response = super().form_valid(form)

        if form.instance.status != original_status:
            admin_emails = settings.EMAIL_ADMINS
            user_email = self.request.user.email
            recipient_list = admin_emails + [user_email]
            subject = 'Sugestão Atualizada'
            message = f'Status da sugestão "{form.instance.title}" foi atualizado para {form.instance.status}.\n\n Att,\n\n Admin 😎'
            
            threading.Thread(target=send_email_async, args=(recipient_list, subject, message)).start()
        return response