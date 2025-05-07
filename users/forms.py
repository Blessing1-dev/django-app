#Import the necessary modules
from django import forms
from django.contrib.auth.models import User
from .models import Student
from itreporting.models import Registration
from django.contrib.auth.forms import UserCreationForm

#Define a class named UserRegisterForm: and Add the additional fields within the class: Email
class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class StudentUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})  # this makes it a browser date picker!
    )
    class Meta:
        model = Student
        fields = ['image', 'date_of_birth', 'address', 'city', 'country']
        
class RegistrationForm(forms.ModelForm):
        class Meta:
            model = Registration
            fields = ['module'] 