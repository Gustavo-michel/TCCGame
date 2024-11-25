from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from app.config import firebase, db
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import login_required
from django.views.decorators.cache import cache_page
import json

auth = firebase.auth()

@cache_page(15 * 1)
def home(request):
    return render(request, 'index.html')


# Users

def register(request):
    if 'uid' in request.session:
        return redirect('account')
    
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
            return redirect('account')
        except Exception as e:
            messages.error(request, f"Erro ao fazer login: {str(e)}")
            return render(request, 'userLogin.html')
    return render(request, 'userLogin.html')

@login_required
def account(request):
    return render(request, 'userAccount.html')


def forgotPassword(request):
    if 'uid' in request.session:
        return redirect('account')

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            auth.generate_password_reset_link(email)
            messages.success(request, "Um e-mail de redefinição de senha foi enviado. Verifique sua caixa de entrada.")
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, f'Erro ao enviar e-mail de redefinição de senha: {e}')
            return redirect(reverse('forgotPassword'))
    
    return render(request, 'userForgot.html')

@login_required
def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')


def privacy(request):
    return render(request, 'privacy.html')

def get_user_id(request):
    user_id = request.user['uid'] if request.user.is_authenticated else None
    return JsonResponse({'user_id': user_id})

# Score logic

@csrf_exempt
def update_user_score(request):
    user_id = request.user['uid']

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
    user_id = request.user['uid']
    
    user_data = db.child("users").child(user_id).get().val()
    
    if not user_data:
        user_data = {"points": 0, "level": 1}
    
    return JsonResponse(user_data)

@login_required
def home_data(request):
    user_data = None 
    
    if 'uid' in request.session:
        user_id = request.user['uid']
        user_data = db.child("users").child(user_id).get().val()
        
        if not user_data:
            user_data = {"points": 0, "level": 1}

        users = db.child("users").order_by_child("points").get().val()

        sorted_users = sorted(users.items(), key=lambda x: x[1]['points'], reverse=True)

        top_positions = [
            {"rank": i + 1, "name": user[1]["name"], "points": user[1]["points"]}
            for i, user in enumerate(sorted_users[:3])
        ]

        position = next((i + 1 for i, user in enumerate(sorted_users) if user[0] == user_id), None)
        
        return JsonResponse({
            "level": user_data["level"],
            "position": position,
            "points": user_data["points"],
            "top_positions": top_positions
        })


# Games

@login_required
def gameHangman(request):
    return render(request, 'gameHangman.html')


@login_required
def gameMemory(request):
    return render(request, 'gameMemory.html')

@login_required
def gameWordle(request):
    return render(request, 'gameWordle.html')

@login_required
def gameLinguage(request):
    return render(request, 'gameLinguage.html')

# ------------------------Adicionei esse código------------------------

def index(request):
    user_points = 0
    if 'uid' in request.session:
        # Busque os pontos do usuário no banco de dados
        user = User.objects.get(uid=request.session['uid'])
        user_points = user.points  # ou como quer que você armazene os pontos
    
    return render(request, 'index.html', {'user_points': user_points})
