# Generated by Django 3.2.6 on 2022-02-20 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_auto_20220220_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='Unknown', max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='Unknown', max_length=70, null=True),
        ),
    ]
