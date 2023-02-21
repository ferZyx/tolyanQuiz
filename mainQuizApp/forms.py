from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UploadedFile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Введите логин',
                               widget=forms.TextInput(
                                   attrs={'placeholder': 'Tolyan', 'class': 'form-control', 'type': 'text'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Введите email', widget=forms.EmailInput(attrs={'placeholder': 'qwerty@email.com'}))
    username = forms.CharField(label='Введите логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
