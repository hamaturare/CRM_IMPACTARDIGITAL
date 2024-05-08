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

class SubmitSuggestionView(LoginRequiredMixin, CreateView):
    model = Suggestion
    form_class = SuggestionForm
    template_name = 'ideabox/submit_suggestion.html'
    success_url = reverse_lazy('suggestions_list')
    
    def post(self, request, *args, **kwargs):
        # Adiciona a mensagem antes de processar o formulário
        messages.success(self.request, 'Sugestão Enviada Com Sucesso')
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

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
