from django.utils.translation import gettext, gettext_lazy as _
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from core.models import ContactModelForm, Register, Attendance
from django.views import View


class SignupForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Confirm Password(Again)',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email', }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(
                                   attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModelForm  # Make sure to use the correct model here
        fields = ['username', 'email', 'Phone_number', 'desc']
        labels = {
            'username': 'Name',
            'email': 'Email',
            'Phone_number': 'Phone number',
            'desc': 'How can I help you',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'icon': 'fas fa-user'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'icon': 'fas fa-envelope'}),
            'Phone_number': forms.TextInput(attrs={'class': 'form-control', 'icon': 'fas fa-phone'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'icon': 'fas-solid fa-question'}),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['first_name', 'last_name', 'fathers_name', 'Phone_number', 'email',
                  'address', 'street', 'city', 'designation', 'qualification', 'computer_knowledge',
                  'course', 'trainer']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = '__all__'
