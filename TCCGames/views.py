from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from firebase_admin import auth


def home(request):
    return render(request, 'home/index.html')

# Usuarios
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = auth.create_user(
                uid=name,
                email=email,
                password=password,
                email_verified=False,
            )
            auth.generate_email_verification_link(user.email)
            messages.success(request, f'Usuário criado com sucesso: {user.uid}')
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {e}')
            return render(request, 'register/register.html', {'error': 'Erro ao criar usuário. Tente novamente.'})
    
    return render(request, 'register/register.html', {'error': None})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = auth.get_user_by_email(email)
            if user and user.email_verified:
                auth_user = authenticate(request, email=email, password=password)
                if auth_user:
                    auth_login(request, auth_user)
                    messages.success(request, f'Usuário logado com sucesso: {user.uid}')
                    return redirect(reverse('account'))
                else:
                    return "Senha incorreta"
            else:
                return "E-mail não verificado"
        except Exception as e:
            messages.error(request, f'Erro ao fazer login: {e}')
            return render(request, 'login/login.html', {'error': 'Erro ao fazer login. Verifique suas credenciais.'})
    
    return render(request, 'login/login.html', {'error': None})

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        try:
            auth.generate_password_reset_link(email)
            messages.success(request, "Um e-mail de redefinição de senha foi enviado. Verifique sua caixa de entrada.")
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, f'Erro ao enviar e-mail de redefinição de senha: {e}')
            return redirect(reverse('forgotPassword'))
    
    return render(request, 'forgotpassword/forgotPassword.html')

def account(request):
    if request.user.is_authenticated:
        return render(request, 'account/account.html')
    else:
        return redirect(reverse('login'))

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))

# Games

def gameHangman(request):
    return render(request, 'gameHangman/hangman.html')

def gameMemory(request):
    return render(request, 'gameMemory/memory.html')

def gameWordle(request):
    return render(request, 'gameWordle/wordle.html')