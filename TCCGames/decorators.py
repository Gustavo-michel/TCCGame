from django.shortcuts import redirect
from django.contrib import messages
from firebase_admin import auth as firebase_auth

def login_required(function):
    """
    Decorator to restrict access to logged-in users by verifying Firebase ID token.
    """
    def wrap(request, *args, **kwargs):
        print(f"uid request para {request.path}")
        if 'uid' in request.session:
            uid = request.session['uid']
            print(f'UID encontrado: {uid[:10]}')
            try:
                decoded_token = firebase_auth.verify_id_token(uid, clock_skew_seconds=10)
                request.user = {
                    'user_id': decoded_token['uid'],
                    'email': decoded_token.get('email'),
                    'name': decoded_token.get('name'),
                }
                return function(request, *args, **kwargs)
            except firebase_auth.ExpiredIdTokenError:
                messages.error(request, 'Sua sessão expirou. Faça login novamente.')
            except firebase_auth.InvalidIdTokenError:
                messages.error(request, 'Token inválido. Por favor, faça login novamente.')
            except Exception as e:
                messages.error(request, f'Erro ao validar sessão: {str(e)}')
            return redirect('login')
        else:
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
