from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm


"""montre tous les posts classés par date de création inverse"""
def post_list(request):
    posts = Post.objects.all().order_by('-date_creation')
    return render(request, 'blog/post_list.html', {'posts':posts})

"""affiche un post spécifique ciblé par son id"""
def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

"""formulaire pour créer un nouveau post"""
@login_required
def post_new(request):
    # les données ont été saisies dans le formulaire
    if request.method == "POST":
        form = PostForm(request.POST)
        # si tous les champs obligatoires ont été remplis et aucune valeur incorrecte n'a été envoyée
        if form.is_valid():
            post = form.save(commit=False)
            post.auteur = request.user
            post.date_creation = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    # on accède à la page pour la première fois et nous voulons un formulaire vide
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

"""modifie un post"""
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.auteur = request.user
            post.date_creation = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

"""supprime un post"""
@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

"""ajoute un commentaire à un post"""
@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.auteur = request.user
            if request.user.is_superuser:
                comment.approuver()
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

"""approuve le commentaire"""
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approuver()
    return redirect('post_detail', pk=comment.post.pk)

"""supprime le commentaire"""
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)
