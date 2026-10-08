from django import forms

from .models import Client


class ClientRegistrationForm(forms.Form):
    entity_type = forms.ChoiceField(label="Tipo", choices=Client.EntityType.choices)
    tax_id = forms.CharField(label="CPF/CNPJ", max_length=18)
    legal_name = forms.CharField(label="Razão social/nome", max_length=255)
    trade_name = forms.CharField(label="Nome fantasia", max_length=255, required=False)
    service_scope = forms.ChoiceField(label="Atuação", choices=Client.ServiceScope.choices)
    email = forms.EmailField(required=False)
    phone = forms.CharField(label="Telefone", max_length=30, required=False)
    start_of_service = forms.DateField(
        label="Início do atendimento", widget=forms.DateInput(attrs={"type": "date"})
    )
