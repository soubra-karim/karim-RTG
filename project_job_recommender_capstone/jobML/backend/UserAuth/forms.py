from django import forms
from .models import User

class SignupForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    name = forms.CharField(label='name', max_length=100)
    email = forms.EmailField(label='email', max_length=100)
    phone_number = forms.CharField(label='phone_number', max_length=15)
    password = forms.CharField(label='password', widget=forms.PasswordInput(), max_length=100)
    user_type = forms.ChoiceField(choices=User.UserType.choices, label='User Type')
