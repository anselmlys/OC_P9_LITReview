from django import forms

from . import models


class TicketForm(forms.ModelForm):
    title = forms.CharField(label='Titre')

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
