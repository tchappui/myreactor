from django.db import models

class Player(models.Model):
    first_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', 'first_name')

    def __str__(self):
        return f"{self.first_name} {name}"
