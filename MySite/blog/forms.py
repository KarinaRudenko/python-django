from django import forms
from .models import Comment, New
from django.contrib.auth.forms import SetPasswordForm
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django.forms.widgets import ClearableFileInput

class NewForm(ModelForm):
    class Meta:
        model = New
        fields = {'title', 'text', 'deck', 'data', 'author', 'image'}
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи'
            }),
            "text": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Текст'
            }),
            "deck": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            "data": DateTimeInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации'
            }),
            "image": ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Изображение'
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'name': 'Имя',
            'email': 'E-mail',
            'body': 'Текст'
        }

class UserPasswordChangeForm(SetPasswordForm):
    """
    Форма изменения пароля
    """
    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
