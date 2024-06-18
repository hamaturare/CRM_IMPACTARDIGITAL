from django.contrib import admin
from .models import ChatbotState, ChatbotQuestion, ChatbotOption

class ChatbotQuestionInline(admin.StackedInline):
    model = ChatbotQuestion
    extra = 1

class ChatbotOptionInline(admin.StackedInline):
    model = ChatbotOption
    extra = 1

@admin.register(ChatbotState)
class ChatbotStateAdmin(admin.ModelAdmin):
    inlines = [ChatbotQuestionInline, ChatbotOptionInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.structure = self.generate_structure(obj)
        obj.save()

    def generate_structure(self, obj):
        structure = {
            'name': obj.name,
            'children': []
        }
        questions = ChatbotQuestion.objects.filter(state=obj)
        for question in questions:
            question_dict = {
                'name': question.question_text,
                'children': []
            }
            options = ChatbotOption.objects.filter(question=question)
            for option in options:
                option_dict = {
                    'name': option.option_text,
                    'response_message': option.response_message,
                    'next_state': option.next_state.name if option.next_state else None
                }
                question_dict['children'].append(option_dict)
            structure['children'].append(question_dict)
        return structure

admin.site.register(ChatbotQuestion)
admin.site.register(ChatbotOption)
