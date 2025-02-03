# accounts/views.py
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm , PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import views as auth_views

def login_view(request):
    username = ''  # Initialize username
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Check if the user exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Invalid password. Please try again.')
            else:
                messages.error(request, 'No user found with this username.')
    
    return render(request, 'accounts/login.html', {'username': username})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=email))
            
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.html"
                    context = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Your Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    }
                    email_content = render_to_string(email_template_name, context)
                    
                    try:
                        send_mail(
                            subject,
                            email_content,
                            'your-email@gmail.com',  # Replace with your email
                            [user.email],
                            fail_silently=False,
                        )
                        messages.success(request, 
                            "Password reset link has been sent to your email address.")
                        return redirect('password_reset_done')
                        
                    except BadHeaderError:
                        messages.error(request, 
                            "An error occurred while sending the email. Please try again later.")
                        return HttpResponse('Invalid header found.')
                    
            else:
                messages.error(request, 
                    "No user is associated with this email address.")
                
    else:
        form = PasswordResetForm()
    
    return render(request, 'accounts/forgot_pass.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            if request.user.check_password(old_password):
                request.user.set_password(new_password)
                request.user.save()
                messages.success(request, 'Password changed successfully!')
                return redirect('login')
            else:
                messages.error(request, 'Old password is incorrect.')
        else:
            messages.error(request, 'New passwords do not match.')
    return render(request, 'accounts/change_pass.html')

@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'username': request.user.username})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')