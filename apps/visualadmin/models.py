from django.db import models

class ChatbotState(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ChatbotQuestion(models.Model):
    state = models.ForeignKey(ChatbotState, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=(('text', 'Text'), ('choice', 'Choice'), ('number', 'Number')))
    invalid_response_message = models.TextField(blank=True, null=True)
    custom_field_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.question_text


class ChatbotOption(models.Model):
    question = models.ForeignKey(ChatbotQuestion, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=100)
    response_message = models.TextField(blank=True, null=True)
    next_state = models.ForeignKey(ChatbotState, on_delete=models.SET_NULL, blank=True, null=True, related_name='option_next_state')

    def __str__(self):
        return self.option_text
