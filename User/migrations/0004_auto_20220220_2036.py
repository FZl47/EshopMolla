# Generated by Django 3.2.6 on 2022-02-20 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20220220_0651'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
