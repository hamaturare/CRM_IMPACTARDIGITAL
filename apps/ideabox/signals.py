import threading  # Import threading to run email sending in a separate thread
from django.db.models.signals import post_save, pre_save  # Import signals to hook into model save events
from django.dispatch import receiver  # Import receiver to connect signals to functions
from django.core.mail import send_mail  # Import send_mail to send emails
from django.conf import settings  # Import settings to access email configuration
from .models import Suggestion  # Import the Suggestion model
import logging  # Import logging to log information and errors

# Set up a logger to log email sending information and errors
logger = logging.getLogger(__name__)

# Define a function to send emails asynchronously
def send_email_async(subject, message, recipient_list):
    try:
        # Try sending the email
        send_mail(
            subject,  # The subject of the email
            message,  # The message of the email
            settings.EMAIL_HOST_USER,  # The sender's email address
            recipient_list,  # List of recipient email addresses
            fail_silently=False,  # If True, suppress SMTP exceptions
        )
        # Log success message
        logger.info(f"Email sent to {recipient_list}")
    except Exception as e:
        # Log error message if email sending fails
        logger.error(f"Failed to send email to {recipient_list}: {e}")

# This dictionary will store the original status of the Suggestion instances before they are saved
original_status = {}

# Connect the pre_save signal to the capture_original_status function
@receiver(pre_save, sender=Suggestion)
def capture_original_status(sender, instance, **kwargs):
    # If the instance already exists (i.e., it has a primary key)
    if instance.pk:
        try:
            # Retrieve the original instance from the database
            original = sender.objects.get(pk=instance.pk)
            # Store the original status in the original_status dictionary
            original_status[instance.pk] = original.status
        except sender.DoesNotExist:
            # If the instance does not exist in the database, set the original status to None
            original_status[instance.pk] = None

# Connect the post_save signal to the send_suggestion_email function
@receiver(post_save, sender=Suggestion)
def send_suggestion_email(sender, instance, created, **kwargs):
    # Get the admin emails from settings
    admin_emails = settings.EMAIL_ADMINS
    # Get the email of the user who created the suggestion
    user_email = instance.user.email
    # Create a list of recipients (admins and the user)
    recipient_list = admin_emails + [user_email]

    if created:
        # If the instance was just created, prepare the email subject and message
        print(instance)
        print(instance.user)
        print(instance.user.email)
        print(recipient_list)
        print(admin_emails)
        subject = 'Nova Sugestão Recebida'
        message = f'Uma nova sugestão foi submetida por {instance.user.username}. \n\nTítulo: {instance.title}\n\nSugestão: {instance.content}'
        # Start a new thread to send the email asynchronously
        threading.Thread(target=send_email_async, args=(subject, message, recipient_list)).start()
    else:
        # If the instance was updated, check if the status has changed
        if instance.pk in original_status and original_status[instance.pk] != instance.status:
            print(instance)
            print(instance.user)
            print(instance.user.email)
            print(recipient_list)
            print(admin_emails)
            # Prepare the email subject and message for status update
            subject = 'Sugestão Atualizada'
            message = f'Status da sugestão "{instance.title}" foi atualizado para {instance.status.name}.'
            # Start a new thread to send the email asynchronously
            threading.Thread(target=send_email_async, args=(subject, message, recipient_list)).start()
        # Clean up the dictionary by removing the instance's entry
        if instance.pk in original_status:
            del original_status[instance.pk]
