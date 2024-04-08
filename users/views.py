from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserProfileForm, UserRegistrationForm, EmailForm
from .models import UserProfile

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm() 
    return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = None

    try:
        user_email = request.user.email
    except User.DoesNotExist:
        user_email = None

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        email_form = EmailForm(request.POST, instance=request.user)
        if profile_form.is_valid() and email_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            email_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=profile)
        email_form = EmailForm(instance=request.user, initial={'email': user_email})
    return render(request, 'users/edit.html', {'profile_form': profile_form, 'email_form': email_form})