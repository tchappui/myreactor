from django import forms

from players.models import Player

class PlayerForm(forms.Form):
    email = forms.EmailField(label="Votre adresse e-mail")
    first_name = forms.CharField(label="Votre prénom", max_length=255)
    name = forms.CharField(label="Votre nom", max_length=255)
    