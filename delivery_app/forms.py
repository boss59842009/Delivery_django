from django.forms import ModelForm
from delivery_app.models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number']

