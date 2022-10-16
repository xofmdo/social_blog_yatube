from django import forms
from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):
    """Форма для создания поста."""
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10, 'cols': 40}),
        }
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа поста',
        }


class CommentForm(ModelForm):
    """Форма для создания комментария к посту."""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'cols': 80, 'rows': 5})
        }
