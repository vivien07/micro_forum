from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    # champ texte avec un nombre limité de caractères.
    titre = models.CharField(max_length=200)
    # champ texte sans limite de caractères
    texte = models.TextField()
    # champ horodatage (date et heure
    date_creation = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titre

    def commentaires_approuves(self):
        return self.commentaires.filter(approuve=True)


class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    texte = models.TextField()
    date_creation = models.DateTimeField(default=timezone.now)
    approuve = models.BooleanField(default=False)

    def approuver(self):
        self.approuve = True
        self.save()

    def __str__(self):
        return self.texte