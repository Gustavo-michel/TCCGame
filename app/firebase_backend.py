from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from firebase_admin import auth

class FirebaseBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            token = request.POST.get('idToken')
            if token:
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
                user = auth.get_user(uid)
                if user and user.email_verified:
                    # Se necessário, crie um usuário Django
                    django_user, created = User.objects.get_or_create(username=user.email, defaults={'email': user.email})
                    return django_user
        except Exception as e:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
