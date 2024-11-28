from django.contrib import admin
from django.urls import path
from TCCGames import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('registrar/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout, name='logout'),
    path('gameHangman/', views.gameHangman, name='gameHangman'),
    path('gameMemory/', views.gameMemory, name='gameMemory'),
    path('gameWordle/', views.gameWordle, name='gameWordle'),
    path('gameLinguage/', views.gameLinguage, name='gameLinguage'),
    path('privacy/', views.privacy, name='privacy'),
    # Endpoints
    path('update_score/', views.update_user_score, name='update_score'),
    path('recover_user_data/', views.recover_user_data, name='recover_user_data'),
    path('home_data/', views.home_data, name='home_data'),
]
