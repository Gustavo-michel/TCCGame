from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from firebase_admin import auth as firebase_auth

def login_required(function):
    def wrap(request, *args, **kwargs):
        if 'uid' in request.session:
            try:
                uid = request.session['uid']
                decoded_token = firebase_auth.verify_id_token(uid)
                request.user = decoded_token
            except Exception:
                messages.error(request, 'Sessão expirada ou inválida. Faça login novamente.')
                return redirect('login')
            return function(request, *args, **kwargs)
        else:
            messages.error(request, 'Você precisa estar logado para acessar esta página.')
            return redirect('login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
