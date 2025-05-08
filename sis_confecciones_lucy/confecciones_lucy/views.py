# confecciones_lucy/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base')  
        else:
            messages.error(request, "Credenciales incorrectas.")
    return render(request, 'login.html')

def base_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  
    return render(request, 'base.html')
