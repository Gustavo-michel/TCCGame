from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from firebase_admin import auth

def home(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
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
            return render(request, 'userRegister.html', {'error': 'Erro ao criar usuário. Tente novamente.'})
    
    return render(request, 'userRegister.html', {'error': None})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            user_django = authenticate(request, email=email, password=password)

            if user_django is not None:
                auth_login(request, user_django)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('account')
            else:
                new_user_django = User.objects.create_user(email=email, password=password)
                auth_login(request, new_user_django)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('account')
        except Exception as e:
            messages.error(request, f'Erro ao fazer login: {e}')
            return render(request, 'userLogin.html', {'error': 'Credenciais inválidas. Tente novamente.'})
        
    return render(request, 'userLogin.html', {'error': None})

def account(request):
    if request.user.is_authenticated:
        return render(request, 'userAccount.html')
    else:
        return redirect(reverse('login'))


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
    
    return render(request, 'userForgot.html')

def logout(request):
    auth_logout(request)
    return redirect(reverse('login'))

# Games

def gameHangman(request):
    return render(request, 'gameHangman.html')

def gameMemory(request):
    return render(request, 'gameMemory.html')

def gameWordle(request):
    return render(request, 'gameWordle.html')

def gameLinguage(request):
    return render(request, 'gameLinguage.html')

def privacy(request):
    return render(request, 'privacy.html')