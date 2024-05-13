from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'  # Utilizar todos os campos

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        # Campos que você não deseja que sejam editáveis
        readonly_fields = ['created_at', 'id']  # Adicione mais campos conforme necessário

        # Aplicar a propriedade de readonly para os campos desejados
        for field_name in readonly_fields:
            if field_name in self.fields:
                self.fields[field_name].disabled = True  # Desativa o campo, mantendo-o visível mas não editável