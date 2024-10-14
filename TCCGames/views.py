from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from firebase_admin import auth
from .models import Score

def home(request):
    return render(request, 'index.html')

# Users

def register(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'O e-mail já está registrado.')
                return render(request, 'userRegister.html', {'error': 'O e-mail já está registrado.'})

            user_django = User.objects.create_user(
                username=name,
                email=email, 
                password=password
            )

            user = auth.create_user(
                display_name=name,
                email=email,
                password=password,
                email_verified=False,
            )
            auth.generate_email_verification_link(user.email)

            messages.success(request, f'Usuário criado com sucesso: {user.display_name}.  Verifique seu email: {user_django.email} para completar a verificação.')
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, f'Erro ao criar usuário: {e}')
            return render(request, 'userRegister.html', {'error': 'Erro ao criar usuário. Tente novamente.'})
    
    return render(request, 'userRegister.html', {'error': None})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Email: {email}")
        print(f"Password: {password}")

        try:
            user_django = authenticate(request, email=email, password=password)
            print(f"User Django: {user_django}")

            firebase_user = auth.get_user_by_email(email)
            print(f"Firebase User: {firebase_user}")

            if user_django is not None and firebase_user is not None:
                auth_login(request, user_django)
                messages.success(request, 'Login realizado com sucesso!')
                return redirect('account')
            else:
                print("User Django ou Firebase User é None")
                messages.error(request, 'Credenciais inválidas ou usuário não registrado.')
                return redirect('register')
        except Exception as e:
            messages.error(request, f'Erro ao fazer login: {e}')
            return render(request, 'userLogin.html', {'erro': 'Credenciais inválidas. Tente novamente.'})
        
    return render(request, 'userLogin.html', {'error': None})

@login_required
def account(request):
    scores = Score.objects.filter(user=request.user)
    total_score = sum(score.points for score in scores) 
    return render(request, 'userAccount.html', {'scores': scores, 'total_score': total_score})


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


def privacy(request):
    return render(request, 'privacy.html')

# Games

def update_score(user, points):
    score, created = Score.objects.get_or_create(user=user)
    score.points += points
    score.save()
    return score.points

@login_required
def gameHangman(request):
    points = 10

    total_points = update_score(request.user, points)

    return render(request, 'gameHangman.html', {'points': total_points})

@login_required
def gameMemory(request):
    points = 10

    total_points = update_score(request.user, points)
    return render(request, 'gameMemory.html', {'points': total_points})

@login_required
def gameWordle(request):
    points = 10

    total_points = update_score(request.user, points)
    return render(request, 'gameWordle.html', {'points': total_points})

@login_required
def gameLinguage(request):
    points = 10

    total_points = update_score(request.user, points)
    return render(request, 'gameLinguage.html', {'points': total_points})