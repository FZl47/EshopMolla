# Generated by Django 3.2.6 on 2022-02-20 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='unknown', max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='unknown', max_length=70, null=True),
        ),
    ]
