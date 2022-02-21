# Generated by Django 3.2.6 on 2022-02-18 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Transportation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipping',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=12),
            preserve_default=False,
        ),
    ]