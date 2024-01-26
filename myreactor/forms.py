from django import forms
from django.core.exceptions import ValidationError

from .players.models import Player


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ("name",)
