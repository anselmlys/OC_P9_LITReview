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


class ReviewForm(forms.ModelForm):
    CHOICES = [
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    headline = forms.CharField(label='Titre')
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    body = forms.CharField(widget=forms.Textarea, label='Commentaire')

    class Meta:
        model = models.Review
        fields = ['headline', 'body', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
