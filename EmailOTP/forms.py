from django import forms
from .models import EmailOTP

class EmailOTPForm(forms.ModelForm):
    class Meta:
        model = EmailOTP
        fields = ['email', 'otp']