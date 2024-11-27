from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from app.config import firebase, db
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import auth as admin_auth
from .decorators import login_required
from django.views.decorators.cache import cache_page
import json

auth = firebase.auth()

# @cache_page(15 * 1)
def home(request):
    return render(request, 'index.html')


# ---------- Users ----------

def register(request):
    '''
    Registra um novo usuário no sistema utilizando email e senha para autenticação no firebase.
    '''
    if 'uid' in request.session:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        verifyPassword = request.POST.get('confirm-password')

        if password != verifyPassword:
            messages.error(request, 'As senhas não coincidem!')
            return redirect('register')

        try:
            user = auth.create_user_with_email_and_password(email, password)
            messages.success(request, f'Usuário {name} registrado com sucesso!')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Erro ao registrar: {str(e)}')
            return redirect('register')

    return render(request, 'userRegister.html')

def login(request):
    '''
    Realiza o login de um usuário no sistema utilizando email e senha para autenticação no firebase, salva o token de autenticação na sessão do usuário.
    '''
    if 'uid' in request.session:
        return redirect('account')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Erro ao fazer login: {str(e)}")
            return render(request, 'userLogin.html')
    return render(request, 'userLogin.html')

@login_required
def account(request):
    '''
    Renderiza a página de conta do usuário.
    '''
    return render(request, 'userAccount.html')


def forgotPassword(request):
    '''
    Envia um e-mail de redefinição de senha para o email do usuário.
    '''
    if 'uid' in request.session:
        return redirect('account')

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            admin_auth.generate_password_reset_link(email)
            messages.success(request, "Um e-mail de redefinição de senha foi enviado. Verifique sua caixa de entrada.")
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, f'Erro ao enviar e-mail de redefinição de senha: {e}')
            return redirect(reverse('forgotPassword'))
    
    return render(request, 'userForgot.html')

@login_required
def logout(request):
    '''
    Realiza o logout do usuário, removendo o token de autenticação da sessão.
    '''
    try:
        del request.session['uid']
    except KeyError:
        pass
    messages.success(request, 'Logout realizado com sucesso!')
    print("Logout realizado com sucesso!")
    return redirect('login')


def privacy(request):
    '''
    Renderiza a página de política de privacidade do site.
    '''
    return render(request, 'privacy.html')

def get_user_id(request):
    '''
    Retorna o ID do usuário autenticado.
    '''
    if hasattr(request, 'user') and not request.user.is_anonymous:
        user_id = request.user.get('user_id', None)
    else:
        user_id = None
    return JsonResponse({'user_id': user_id})

# ---------- Score logic ----------

@csrf_exempt
@login_required
def update_user_score(request):
    '''
    Atualiza o score do usuário no banco de dados do firebase.
    '''
    user_id = request.user.get('user_id')

    if request.method == 'POST':

        data = json.loads(request.body)
        points_earned = data.get('points_earned', 0)

        user_data = db.child("users").child(user_id).get().val()

        if not user_data:
            current_points = 0
            current_level = 1
        else:
            current_points = user_data['points']
            current_level = user_data['level']

        points = current_points + points_earned
        level = points // 100 + 1

        # Atualiza os dados do usuário no Firebase
        db.child("users").child(user_id).update({
            "points": points,
            "level": level
        })

        return JsonResponse({"points": points, "level": level})
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)
    
# Recupera os dados do usuario para listagem
@csrf_exempt
def recover_user_data(request):
    '''
    Recupera os dados do usuário para listagem.
    '''
    user_id = request.user.get('user_id')
    
    user_data = db.child("users").child(user_id).get().val()
    
    if not user_data:
        user_data = {"points": 0, "level": 1}
    
    return JsonResponse(user_data)

@login_required
def home_data(request):
    '''
    Recupera os dados do usuário para listagem na página inicial.
    '''
    user_data = None 
    
    if 'uid' in request.session:
        user_id = request.user.get('user_id')
        try:
            user_data = db.child("users").child(user_id).get().val()
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=401)

        if not user_data:
            user_data = {"points": 0, "level": 1}
        
        return JsonResponse({
            "level": user_data["level"],
            "points": user_data["points"],
        })
    else:
        return JsonResponse({"error": "Usuário não autenticado"}, status=401)


# ---------- Games ----------

@login_required
def gameHangman(request):
    '''
    Renderiza a página do jogo da forca.
    '''
    return render(request, 'gameHangman.html')


@login_required
def gameMemory(request):
    '''
    Renderiza a página do jogo da memória.
    '''
    return render(request, 'gameMemory.html')

@login_required
def gameWordle(request):
    '''
    Renderiza a página do jogo da palavra.
    '''
    return render(request, 'gameWordle.html')

@login_required
def gameLinguage(request):
    '''
    Renderiza a página do jogo de linguagem.
    '''
    return render(request, 'gameLinguage.html')