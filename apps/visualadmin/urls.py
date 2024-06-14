# apps/visualadmin/urls.py
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.visualadmin), name='visualadmin'),
    path('add-state/', views.add_state, name='add_state'),
    path('edit-state/', views.edit_state, name='edit_state'),
    path('delete-state/', views.delete_state, name='delete_state'),
    path('add-question/', views.add_question, name='add_question'),
    path('edit-question/', views.edit_question, name='edit_question'),
    path('delete-question/', views.delete_question, name='delete_question'),
    path('add-option/', views.add_option, name='add_option'),
    path('edit-option/', views.edit_option, name='edit_option'),
    path('delete-option/', views.delete_option, name='delete_option'),
]
