from django import forms
from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UploadedFile


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Введите email',
                               widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control', 'type':'email'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Введите email', widget=forms.TextInput(attrs={'placeholder': 'qwerty@email.com', 'type':'email'}))
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
