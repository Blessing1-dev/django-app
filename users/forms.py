#Import the necessary modules
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#Define a class named UserRegisterForm: and Add the additional fields within the class: Email
class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']