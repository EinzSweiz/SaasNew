from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, User
from cfehome.tasks import send_email_task


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    return render(request, 'auth/login.html', {})


def register_view(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():       
            user = form.save()
            login(request, user)
            
            subject = f'Hello {user.username}'
            message = f'Hi {user.first_name},\n\nThank you for registering on our site!'
            recipient_list = [user.email]
            send_email_task.delay(subject=subject,
                            message=message,
                            recipient_list=recipient_list)
            return redirect('/')
    else:
        form = UserForm()
        
    return render(request, 'auth/register.html', {'form':form} )


def logout_view(request):
    logout(request)
    return redirect('user:login_view')