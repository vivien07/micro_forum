from django.contrib import admin
from .models import Post

# enregistre le modèle et le rend visible dans l'interface d'administration
admin.site.register(Post)