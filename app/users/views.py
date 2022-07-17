from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth





def singup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if not password == confirm_password:
            messages.info(request, 'Both passwords are not matching')
            return redirect(singup)
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken')
            return redirect(singup)
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already taken')
            return redirect(singup)
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        auth.login(request, user)
        return redirect('main')
    elif request.method == 'GET':
        return render(request, 'users/registration.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')
        auth.login(request, user)
        return redirect('main')
    elif request.method == 'GET':
        return render(request, 'users/login.html')


def logout_user(request):
    auth.logout(request)
    return redirect('main')

