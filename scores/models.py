from django.db import models

from casestudy.models import CaseStudy
from players.models import Player

class Score(models.Model):
    total_reaction_time = models.FloatField(null=False)
    final_conversion = models.FloatField(null=False)
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE,
        related_name='scores'
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"({self.player}, {self.total_reaction_time}, {self.final_conversion:.2f})"

