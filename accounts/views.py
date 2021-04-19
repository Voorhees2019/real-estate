from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from contacts.models import Contact


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html', {})


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('login')
                    # Login after register
                    # auth.login(request, user)
                    # messages.success(request, f'You are now logged in')
                    # return redirect('index')
        else:
            messages.error(request, f'Passwords did not match')
            return redirect('register')
    return render(request, 'accounts/register.html', {})


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')


@login_required
def dashboard(request):
    user_contacts = Contact.objects.filter(user=request.user.id).order_by('-contact_date')
    return render(request, 'accounts/dashboard.html', {'contacts': user_contacts})
