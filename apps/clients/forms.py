from django import forms
from .models import Client, ClientLeads

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

        # Remover o campo 'status' do formulário para as views de adição e atualização
        if 'status' in self.fields:
            self.fields['status'].widget = forms.HiddenInput()
                
class ClientLeadsForm(forms.ModelForm):
    class Meta:
        model = ClientLeads
        fields = '__all__'
        exclude = ['client']  #Exclua 'lead' do formulário