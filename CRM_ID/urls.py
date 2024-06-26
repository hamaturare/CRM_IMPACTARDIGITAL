from django.contrib import admin
from django.urls import path, include

from apps.common.views import *
from apps.leads.views import *
from apps.clients.views import *
from django.contrib.auth import views as auth_views
from apps.ideabox.views import *
from apps.wpmessages.views import *
from apps.userprofile.views import preview_template

urlpatterns = [

    path('admin/', admin.site.urls),
    
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Authentication 
    # path('register/', SignUpView.as_view(), name="register"),

    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'
        ),
        name='login'
    ),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
        ),
        name='logout'
    ),

    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='common/change-password.html',
            success_url='/'
        ),
        name='change-password'
    ),

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
             subject_template_name='common/password-reset/password_reset_subject.txt',
             email_template_name='common/password-reset/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    #LEADS
    path('leads/',LeadsView.as_view(), name='leads'),  
    path('update_lead/<int:pk>/', LeadUpdateView.as_view(), name='update_lead'),
    path('delete_lead/<int:pk>/', LeadDeleteView.as_view(), name='delete_lead'),
    path('add_lead/', AddLeadView.as_view(), name='add_lead'),
    path('lead_info/<int:pk>/', LeadDetailView.as_view(), name='lead_info'),
    path('delete_followup/<int:pk>/', FollowUpDeleteView.as_view(), name='delete_followup'),
    
    #CLIENTS
    path('clients/',ClientsView.as_view(), name='clients'),
    path('update_client_status_listview/<int:pk>/', update_client_status_listview, name='update_client_status_listview'),
    path('update_client_status_client_info/<int:pk>/', update_client_status_client_info, name='update_client_status_client_info'),
    path('client_info/<int:pk>/', ClientDetailView.as_view(), name='client_info'),
    path('update_client/<int:pk>/', ClientUpdateView.as_view(), name='update_client'),
    path('delete_client/<int:pk>/', ClientDeleteView.as_view(), name='delete_client'),
    path('add_client/', AddClientView.as_view(), name='add_client'),
    path('migrate_client_lead/<int:pk>/', MigrateClientLeadView.as_view(), name='migrate_client_lead'),
     
    #IDEABOX
    path('submit_suggestion/', SubmitSuggestionView.as_view(), name='submit_suggestion'),
    path('suggestions/', SuggestionsListView.as_view(), name='suggestions_list'),
    path('update_suggestion/<int:pk>/', SuggestionUpdateView.as_view(), name='view_suggestion'),
    path('preview/', preview_template, name='index'),

    #MESSAGES
    path('messages/', WpMessagesView.as_view(), name='wpmessages'),
    path('f2ebd9bb-3e10-494b-80d1-45a7b5a11d02/', whatsapp_webhook, name='whatsapp-webhook'),
    path('update_contacted_status/<int:wpmessage_id>/', update_contacted_status, name='update_contacted_status'),
    path('delete_wpmessage/<int:pk>/', DeleteWpMessageView.as_view(), name='delete_wpmessage'),
    path('migrate_to_leads/<int:pk>/', MigrateToLeadView.as_view(), name='migrate_to_leads'),

    #VISUAL ADMIN
    path('chatbot/', include('apps.visualadmin.urls')),

]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
