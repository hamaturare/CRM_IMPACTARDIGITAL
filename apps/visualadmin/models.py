from django.db import models

class ChatbotState(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class ChatbotQuestion(models.Model):
    state = models.ForeignKey(ChatbotState, on_delete=models.CASCADE, related_name='questions') #Stagio que a pergunta se encontra
    question_text = models.TextField() # Texto da pergunta que vai ser mandada ao usuario
    question_type = models.CharField(max_length=50, choices=(('text', 'Text'), ('choice', 'Choice'), ('number', 'Number'))) #Tipo da pergunta
    invalid_response_message = models.TextField(blank=True, null=True) # Texto da pergunta que vai ser enviada caso o usuario digite uma opcao errada errada
    custom_field_name = models.CharField(max_length=100, blank=True, null=True) # Aqui pode adicionar a variavel que vai ser linked com o db do Leads depois ou deixar em branco

    def __str__(self):
        return self.question_text


class ChatbotOption(models.Model):
    question = models.ForeignKey(ChatbotQuestion, on_delete=models.CASCADE, related_name='options') # Questao a qual a pergunta ta lincada
    option_text = models.CharField(max_length=100) # Aqui vai o valor da resposta que vai ser recebida pelo usuario.
    response_message = models.TextField(blank=True, null=True) # Texto que pode ser enviado de volta ao usuario, este texto vai ser concatenado com a proxima pergunta, pode deixar em branco
    next_state = models.ForeignKey(ChatbotState, on_delete=models.SET_NULL, blank=True, null=True, related_name='option_next_state') # caso aja um proxio estagio a com perguntas vc deve ligar aqui.

    def __str__(self):
        return self.option_text
