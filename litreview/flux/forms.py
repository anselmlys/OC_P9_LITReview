from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from . import models


class TicketForm(forms.ModelForm):
    title = forms.CharField(label='Titre',
                            max_length=128,
                            error_messages={
                                'required': "Veuillez ajouter un titre",
                                'max_length': "Ne doit pas dépasser les 128 caractères."
                            })

    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
        error_messages = {
            'description': {
                'max_length': "Ne doit pas dépasser les 2048 caractères."
            }
        }

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

    headline = forms.CharField(label='Titre',
                               max_length=128,
                               error_messages={
                                'required': "Veuillez ajouter un titre",
                                'max_length': "Ne doit pas dépasser les 128 caractères.",
                            })
    rating = forms.ChoiceField(widget=forms.RadioSelect,
                               choices=CHOICES)
    body = forms.CharField(widget=forms.Textarea,
                           label='Commentaire',
                           max_length=8192,
                           required=False,
                           error_messages={
                               'max_length': "Ne doit pas dépasser les 8192 caractères.",
                           })

    class Meta:
        model = models.Review
        fields = ['headline', 'body', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""


User = get_user_model()

class UserSubscriptionForm(forms.ModelForm):
    followed_user = forms.CharField(
           label='',
           widget=forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'})
    )

    class Meta:
        model = models.UserFollows
        fields = ['followed_user']

    def clean_followed_user(self):
        username = self.cleaned_data['followed_user'].strip()

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Utilisateur introuvable.")
        
        return user
