from django.shortcuts import redirect
from django.contrib import messages
from firebase_admin import auth as firebase_auth
firebase_auth.generate_password_reset_link
def login_required(function):
    def wrap(request, *args, **kwargs):
        print(request)
        if 'uid' in request.session:
            try:
                uid = request.session['uid']
                print(f'UID encontrado: {uid}')
                decoded_token = firebase_auth.verify_id_token(uid, clock_skew_seconds=10)
                request.user = decoded_token
                print('Token decodificado com sucesso!')
            except Exception as e:
                messages.error(request, f'Sessão expirada ou inválida  {str(e)}. Faça login novamente.')
                return redirect('login')
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
