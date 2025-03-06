from django import forms
from django.core.exceptions import ValidationError

from .players.models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ("name",)


class ResetForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput, label="Mot de passe", required=True
    )

    def clean_password(self):
        password = self.cleaned_data["password"]
        if password != "chemtech":
            raise ValidationError("Mot de passe incorrect")
        return password
