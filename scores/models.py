from django.db import models

from casestudy.models import CaseStudy
from players.models import Player

class Score(models.Model):
    total_reaction_time = models.FloatField(null=False)
    has_exploded = models.BooleanField(null=False, default=False)
    final_conversion = models.FloatField(null=False)
    case_study = models.ForeignKey(
        CaseStudy, 
        on_delete=models.CASCADE,
        related_name='scores'
    )
    player = models.ForeignKey(
        Player, 
        on_delete=models.CASCADE,
        related_name='scores'
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.total_reaction_time, self.has_exploded, self.final_conversion

