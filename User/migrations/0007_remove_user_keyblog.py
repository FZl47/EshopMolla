# Generated by Django 3.2.6 on 2022-03-05 05:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0006_user_keyblog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='keyBlog',
        ),
    ]
