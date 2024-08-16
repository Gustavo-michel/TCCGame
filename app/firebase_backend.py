from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from firebase_admin import auth

class FirebaseBackend(BaseBackend):
    """
    Autentica um usuário usando o idToken do Firebase.
    """
    def authenticate(self, request, email=None, idToken=None):
        try:
            if idToken:
                decoded_token = auth.verify_id_token(idToken)
                uid = decoded_token['uid']
                firebase_user = auth.get_user(uid)

                if firebase_user and firebase_user.email == email:
                    django_user, created = User.objects.get_or_create(
                        username=firebase_user.email,
                        defaults={'email': firebase_user.email}
                    )
                    return django_user
                
        except auth.AuthError as e:
            print(f'Erro de autenticação: {e}')
        except Exception as e:
            print(f'Erro ao autenticar: {e}')
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None