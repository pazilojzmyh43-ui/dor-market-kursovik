from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog, Category, Product


class BootstrapAuthenticationForm(AuthenticationForm):
    """Форма входа. Надписи полей — на русском (лабораторная работа 3)."""
    username = forms.CharField(max_length=254,
                               label='Логин',
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Пароль"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Пароль'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': "Комментарий"}


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'image', 'content')
        labels = {
            'title': 'Заголовок',
            'description': 'Краткое содержание',
            'image': 'Картинка',
            'content': 'Полное содержание',
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'description')
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'short_description', 'full_description', 'price', 'image', 'category')
        labels = {
            'name': 'Название',
            'short_description': 'Краткое описание',
            'full_description': 'Полное описание',
            'price': 'Цена',
            'image': 'Картинка',
            'category': 'Категория',
        }
