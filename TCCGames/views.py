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


# -------------------- Users --------------------

def register(request):
    '''
    Register a new user in the system using email and password for authentication in firebase.
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
    Realize the login of a user in the system using email and password for authentication in firebase, saving the authentication token in the user's session.
    '''
    if 'uid' in request.session:
        return redirect('account')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email e senha são obrigatórios.')
            return redirect('login')

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session_id = user.uid
            request.session['uid'] = session_id
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('home')
        
        except auth.InvalidPasswordError:
            messages.error(request, 'Senha inválida. Por favor, tente novamente.')
            return redirect('login')
        except auth.UserNotFoundError:
            messages.error(request, 'Usuário não encontrado. Verifique o email ou registre-se.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Erro ao fazer login: {str(e)}')
            return redirect('login')
    return render(request, 'userLogin.html')

@login_required
def account(request):
    '''
    Render the user account page.
    '''
    return render(request, 'userAccount.html')


def forgotPassword(request):
    '''
    Send a password reset email to the user's email.
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
    Release the user's authentication token from the session.
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
    Render the privacy policy page.
    '''
    return render(request, 'privacy.html')

def get_user_id(request):
    """
    Return the authenticated user's ID.
    """
    if hasattr(request, 'user') and isinstance(request.user, dict):
        user_id = request.user.get('user_id', None)
    else:
        user_id = None
        print("Id não encontrado")

    return JsonResponse({'user_id': user_id})

# -------------------- Score logic --------------------

@login_required
def update_user_score(request):
    """
    Update the user's score in the Firebase database.
    """
    user_id = request.user.get('user_id')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            points_earned = int(data.get('points_earned', 0))

            user_data = db.child("users").child(user_id).get().val()

            current_points = user_data.get('points', 0) if user_data else 0
            current_level = user_data.get('level', 1) if user_data else 1

            points = current_points + points_earned
            level = points // 100 + 1

            db.child("users").child(user_id).update({
                "points": points,
                "level": level
            })

            return JsonResponse({"points": points, "level": level})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Dados inválidos no corpo da requisição"}, status=400)
        except Exception as e:
            return JsonResponse({"error": f"Erro ao atualizar pontuação: {str(e)}"}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)
    
# Recover user data for listing
@csrf_exempt
@login_required
def recover_user_data(request):
    """
    Recover the user's data for listing.
    """
    user_id = request.user.get('user_id')
    
    try:
        user_data = db.child("users").child(user_id).get().val()
        if not user_data:
            user_data = {"points": 0, "level": 1}

        return JsonResponse(user_data)
    except Exception as e:
        return JsonResponse({"error": f"Erro ao recuperar dados: {str(e)}"}, status=500)

@login_required
def home_data(request):
    """
    Recover the user's data for listing on the home page.
    """
    user_id = request.user.get('user_id')
    
    try:
        user_data = db.child("users").child(user_id).get().val()
        if not user_data:
            user_data = {"points": 0, "level": 1}

        return JsonResponse({
            "level": user_data["level"],
            "points": user_data["points"],
        })
    except Exception as e:
        return JsonResponse({"error": f"Erro ao recuperar dados da página inicial: {str(e)}"}, status=500)


# -------------------- Games --------------------

@login_required
def gameHangman(request):
    '''
    Render the hangman game page.
    '''
    return render(request, 'gameHangman.html')

@login_required
def gameMemory(request):
    '''
    Render the memory game page.
    '''
    return render(request, 'gameMemory.html')

@login_required
def gameWordle(request):
    '''
    Render the wordle game page.
    '''
    return render(request, 'gameWordle.html')

@login_required
def gameLinguage(request):
    '''
    Render the language game page.
    '''
    return render(request, 'gameLinguage.html')