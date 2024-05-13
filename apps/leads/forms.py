from django import forms
from django.contrib.auth import get_user_model
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        # Define os campos que serão apenas de leitura
        readonly_fields = ['created_at', 'id']  # Adicione mais campos conforme necessário

        # Aplicar a propriedade de readonly para os campos desejados
        for field_name in readonly_fields:
            if field_name in self.fields:
                self.fields[field_name].disabled = True

        # Configuração para permitir seleção do usuário responsável
        User = get_user_model()  # Obter o modelo de usuário atual
        self.fields['responsible'].queryset = User.objects.all()
        self.fields['responsible'].label = "Responsável pela Lead"
        self.fields['responsible'].required = False  # Torna o campo opcional, se necessário
