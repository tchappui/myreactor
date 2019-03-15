from django.db import models

class Player(models.Model):
    first_name = models.CharField(verbose_name="Votre prénom", max_length=255, blank=True)
    name = models.CharField(verbose_name="Votre nom", max_length=255, blank=True)
    email = models.EmailField(verbose_name="Votre adresse e-mail", unique=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', 'first_name')

    def __str__(self):
        return f"{self.id} {self.email} {self.first_name} {self.name}"
