from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from firebase_admin import auth

class FirebaseBackend(BaseBackend):
    """
    Autentica um usuário usando o e-mail e a senha do Firebase.
    """
    def authenticate(self, email=None, password=None):
        try:
            if email and password:
                firebase_user = auth.get_user_by_email(email)
                # Verificar senha com o Django auth
                
                if firebase_user:
                    django_user, created = User.objects.get_or_create(
                        username=firebase_user.uid,
                        defaults={'email': firebase_user.email}
                    )
                    return django_user

        except auth.AuthError as e:
            print(f'Erro de autenticação no Firebase: {e}')
        except Exception as e:
            print(f'Erro ao autenticar: {e}')
        
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
