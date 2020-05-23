from django import forms
from docapp.models import TicketUser, TicketItem
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = TicketUser
        fields = ('username', 'name', 'password1', 'password2')


class TicketAddForm(forms.ModelForm):
    class Meta:
        model = TicketItem
        fields = ['title', 'time', 'date', 'description', 'filed_user', 'assigned_user', 'completed_user', 'status']
