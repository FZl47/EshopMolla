# Generated by Django 3.2.6 on 2022-03-05 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0008_user_keyblog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='keyBlog',
            field=models.CharField(default='95UgOqNpzSF099OYVtt7f0lrmjiwtBSjX1wQmTqU7Q2UkvlrDF', max_length=50),
        ),
    ]