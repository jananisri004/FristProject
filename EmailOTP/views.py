from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import random
from .models import EmailOTP
# Create your views here.

def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return render(request, 'EmailOTP/send_otp.html', 
                        {'error': 'Please enter a valid email address.'})
        
        otp = str(random.randint(100000, 999999)) 
        

        EmailOTP.objects.update_or_create(
            email=email,
            defaults={'otp': otp}
        )
        
    
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP code is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
    
            pass
        
        return render(request, 'EmailOTP/verify_otp.html', {'email': email, 'otp': otp})
    return render(request, 'EmailOTP/send_otp.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')
        
        if not email or not entered_otp:
            return render(request, 'EmailOTP/verify_otp.html',
                        {'email': email, 'error': 'Please enter both email and OTP.'})
        
        try:
            otp_record = EmailOTP.objects.get(email=email)
            if str(otp_record.otp).strip() == str(entered_otp).strip():
            
                otp_record.delete()
                return render(request, 'EmailOTP/success.html', {'email': email})
            else:
                return render(request, 'EmailOTP/verify_otp.html', 
                            {'email': email, 'error': 'Invalid OTP. Please try again.'})
        except EmailOTP.DoesNotExist:
            return render(request, 'EmailOTP/verify_otp.html',
                        {'email': email, 'error': 'Email not found. Please send OTP again.'})
    return redirect('send_otp')

def success(request):
    return HttpResponse("success page")