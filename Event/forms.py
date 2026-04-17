from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Booking
import re


# 🔐 REGISTER FORM (PRO VERSION)
class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }

    # 🔍 EMAIL UNIQUE CHECK
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already registered")
        return email

    # 🔐 PASSWORD VALIDATION
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 6:
            raise ValidationError("Password must be at least 6 characters")

        if not re.search(r"[A-Z]", password):
            raise ValidationError("Must contain at least one uppercase letter")

        if not re.search(r"[0-9]", password):
            raise ValidationError("Must contain at least one number")

        return password

    # 🔁 MATCH PASSWORD
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            raise ValidationError("Passwords do not match")

        return cleaned_data


# 📅 BOOKING FORM (PRO VERSION)
class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['location', 'event_date', 'requirements']

        widgets = {
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '📍 Event Location'
            }),

            'event_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '📝 Special requirements...',
                'rows': 3
            }),
        }
        

    # 📅 VALIDATE FUTURE DATE
    def clean_event_date(self):
        date = self.cleaned_data.get('event_date')

        from datetime import date as today
        if date < today.today():
            raise ValidationError("Event date must be in future")

        return date