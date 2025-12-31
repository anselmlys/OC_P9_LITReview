from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    '''Form used to authenticate a user with username and password.'''
    username = forms.CharField(
        max_length=63, label="Nom d'utilisateur", widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )
    password = forms.CharField(
        max_length=63, label="Mot de passe", widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
    )


class SignupForm(UserCreationForm):
    '''Form used to register a new user.'''
    username = forms.CharField(
        max_length=63, label="Nom d'utilisateur", widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
    )
    password1 = forms.CharField(
        max_length=63, label="Mot de passe", widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
    )
    password2 = forms.CharField(
        max_length=63,
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe"}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username", "password1", "password2"]
