# Generated by Django 5.0.7 on 2024-11-14 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TCCGames', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='score',
        ),
    ]