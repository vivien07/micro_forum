from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # champ texte avec un nombre limité de caractères.
    title = models.CharField(max_length=200)
    # champ texte sans limite de caractères
    text = models.TextField()
    # champ horodatage (date et heure
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title