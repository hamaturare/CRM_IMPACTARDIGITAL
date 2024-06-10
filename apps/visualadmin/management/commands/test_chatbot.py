# apps/visualadmin/management/commands/test_chatbot.py

from django.core.management.base import BaseCommand
from apps.visualadmin.models import ChatbotState, ChatbotQuestion, ChatbotOption
from apps.wpmessages.models import WpMessage

class Command(BaseCommand):
    help = 'Test the chatbot flow'

    def handle(self, *args, **kwargs):
        state = ChatbotState.objects.first()  # Começa com o primeiro estado

        while state:
            question = state.questions.first()
            if not question:
                break

            print(f"Pergunta: {question.question_text}")
            input_text = input("Resposta: ")

            option = question.options.filter(option_text=input_text).first()
            if option:
                print(f"Resposta do Bot: {option.response_message}")
                state = option.next_state
            else:
                print("Resposta inválida, tente novamente.")
