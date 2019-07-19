from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt
import re

def index(request):
    return render(request, "login_app/index.html")
#REGISTER WITH VALIDATIONS IN MODELS
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birthday=request.POST['birthday'], email=request.POST['email'], password=hashed_password)
        request.session['user'] = new_user.id
        return redirect('/success')
#LOGIN WITH LOGIN VALIDATIONS
def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        l_email = User.objects.get(email=request.POST['email'])
        l_password = request.POST['password']
        passwords_match = bcrypt.checkpw(l_password.encode(), l_email.password.encode())
        if passwords_match:
            request.session['user'] = l_email.id
            return redirect('/success')
        else:
            return redirect('/')
#SUCCESSFULLY LOGGED IN / REGISTERED
def success(request):
    if not 'user' in request.session:
        messages.error(request, "You must log in.")
        return redirect('/')
    else:
        return render(request, 'login_app/success.html', {'user': User.objects.get(id=request.session['user'])})
#LOGOUT
def logout(request):
    request.session.clear()
    return redirect('/')
