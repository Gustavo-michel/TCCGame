from django.contrib import admin
from .models import users

@admin.register(users)
class usersAdmin(admin.ModelAdmin):
    pass    