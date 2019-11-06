from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from ..models import *


def login_index(request):
    if request.user.is_authenticated:
        return redirect('courses/')
    else:
        return redirect('account/login')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            new_user = User(name=username)
            new_user.save()
            user = authenticate(username=username, password=password1)
            login(request, user)
            return redirect('login_index')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/registration.html', context)
