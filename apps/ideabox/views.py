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
        # Adiciona a mensagem antes de processar o formulário
        messages.success(self.request, 'Sugestão Enviada Com Sucesso')
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Associa o usuário logado à instância do formulário antes de salvar
        form.instance.user = self.request.user
        response = super().form_valid(form)  # Isso salva o objeto

        # Get the admin emails from settings.EMAIL_ADMINS
        admin_emails = settings.EMAIL_ADMINS

        # Get the user's email
        user_email = self.request.user.email

        # Combine admin emails and the user's email into a flat list
        recipient_list = admin_emails + [user_email]

        # Send email in a new thread to avoid blocking the response
        thread = threading.Thread(target=self.send_email, args=(recipient_list, form.instance))
        thread.start()

        return response

    def send_email(self, recipient_list, suggestion):
        try:
            send_mail(
                'Nova Sugestão Recebida',  # Assunto do email
                'Uma nova sugestão foi submetida por {}. \n\nTítulo: {}\n\nSugestão: {}'.format(
                    self.request.user.username,
                    suggestion.title,
                    suggestion.content
                ),  # Mensagem
                settings.EMAIL_HOST_USER,  # Email do remetente
                recipient_list,  # Lista de emails que receberão a mensagem
                fail_silently=False,  # Se True, suprime as exceções de SMTP
            )
        except Exception as e:
            # Log the error with more details
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

class SuggestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Suggestion
    form_class = SuggestionUpdateForm
    template_name = 'ideabox/view_suggestion.html'
    success_url = reverse_lazy('suggestions_list')

    def form_valid(self, form):
        messages.success(self.request, 'Sugestão atualizada com sucesso!')
        return super().form_valid(form)
