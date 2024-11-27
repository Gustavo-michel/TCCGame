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
    '''
    Return the authenticated user's ID.
    '''
    if hasattr(request, 'user') and not request.user.is_anonymous:
        user_id = request.user.get('user_id', None)
    else:
        user_id = None
    return JsonResponse({'user_id': user_id})

# -------------------- Score logic --------------------

@csrf_exempt
@login_required
def update_user_score(request):
    '''
    Update the user's score in the firebase database.
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

        # Update the user's data in the Firebase database
        db.child("users").child(user_id).update({
            "points": points,
            "level": level
        })

        return JsonResponse({"points": points, "level": level})
    else:
        return JsonResponse({"error": "Método não permitido"}, status=405)
    
# Recover user data for listing
@csrf_exempt
def recover_user_data(request):
    '''
    Recover the user's data for listing.
    '''
    user_id = request.user.get('user_id')
    
    user_data = db.child("users").child(user_id).get().val()
    
    if not user_data:
        user_data = {"points": 0, "level": 1}
    
    return JsonResponse(user_data)

@login_required
def home_data(request):
    '''
    Recover the user's data for listing on the home page.
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