from django import forms
from django.forms import DateTimeInput

from mailing.models import Client, Mailing, Message
from mailing.services import StileFormMixin


class ClientForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'comment']
        #fields = '__all__'


class MailingForm(StileFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(owner=user)

    start_point = forms.DateTimeField(
        label='Время старта',
        required=False,
        widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M')
    )

    stop_point = forms.DateTimeField(
        label='Время окончания',
        required=False,
        widget=DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}, format='%Y-%m-%dT%H:%M')
    )

    class Meta:
        model = Mailing
        exclude = '__all__'


class MessageForm(StileFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'