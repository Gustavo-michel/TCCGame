from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from firebase_admin import auth as firebase_auth
from unittest.mock import patch

from .models import Score


class UserAuthTests(TestCase):
    def setUp(self):
        self.test_user_email = "testuser@example.com"
        self.test_user_password = "password123"
        self.test_user = User.objects.create_user(
            username="testuser",
            email=self.test_user_email,
            password=self.test_user_password
        )

    @patch('firebase_admin.auth.create_user')
    def test_register_user(self, mock_create_user):
        mock_create_user.return_value = firebase_auth.UserRecord(uid="12345")
        
        response = self.client.post(reverse('register'), {
            'name': 'Test User',
            'email': self.test_user_email,
            'password': self.test_user_password,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email=self.test_user_email).exists())
        mock_create_user.assert_called_once_with(display_name='Test User', email=self.test_user_email, password=self.test_user_password, email_verified=False)

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'email': self.test_user_email,
            'password': self.test_user_password,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.wsgi_request.user, self.test_user)

    def test_login_invalid_user(self):
        response = self.client.post(reverse('login'), {
            'email': 'wrong@example.com',
            'password': 'wrongpassword',
        })

        self.assertEqual(response.status_code, 302) 
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_update_score(self):
        self.client.login(email=self.test_user_email, password=self.test_user_password)

        score = Score.objects.create(user=self.test_user, points=0)
        initial_score = score.points
        
        response = self.client.get(reverse('gameHangman'))
        updated_score = Score.objects.get(user=self.test_user).points

        self.assertEqual(updated_score, initial_score + 10)

    def test_access_account_view(self):
        self.client.login(email=self.test_user_email, password=self.test_user_password)
        
        response = self.client.get(reverse('account'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pontuação Total") 


class ScoreModelTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

    def test_create_score(self):
        score = Score.objects.create(user=self.test_user, points=50)
        self.assertEqual(score.user, self.test_user)
        self.assertEqual(score.points, 50)

    def test_update_score_points(self):
        score = Score.objects.create(user=self.test_user, points=10)
        score.points += 20
        score.save()

        updated_score = Score.objects.get(user=self.test_user)
        self.assertEqual(updated_score.points, 30)

# rodar python manage.py test TCCGames.tests.{função}