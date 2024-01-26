from django.db import models


class Player(models.Model):
    name = models.CharField(
        verbose_name="Votre nom", max_length=255, blank=True
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"
