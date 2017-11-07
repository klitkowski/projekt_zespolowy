from django import forms
from app.models import *


class EventForm(forms.ModelForm):
    class Meta:
        model = Wydarzenie
        fields = ('nazwa', 'opis', 'data', 'budynek')


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('kto', 'mieszkaniec', 'opis')
