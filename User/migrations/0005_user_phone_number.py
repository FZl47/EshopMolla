# Generated by Django 3.2.6 on 2022-02-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_auto_20220220_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
