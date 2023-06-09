# Generated by Django 3.2 on 2023-02-21 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houseit', '0003_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=False, max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.TextField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.TextField(blank=True, max_length=150),
        ),
    ]
