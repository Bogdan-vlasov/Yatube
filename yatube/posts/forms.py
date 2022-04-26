from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        labels = {
            'group': 'Группа',
            'text': 'Текст записи',
            'image': 'Изображение',
        }
        help_texts = {
            'group': 'При необходимости выберите группу',
            'text': 'Здесь напишите текст записи',
            'image': 'При необходимости добавьте изображение',
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {
            'text': 'Текст комментария',
        }
        help_texts = {
            'text': 'Здесь напишите комментарий',
        }
