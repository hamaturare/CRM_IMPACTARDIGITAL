# apps/wpmessages/context_processors.py

from .models import WpMessage

def message_count(request):
    return {
        'message_count': WpMessage.objects.count()
    }
