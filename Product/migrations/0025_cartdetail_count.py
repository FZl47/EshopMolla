# Generated by Django 3.2.6 on 2022-02-15 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0024_product_information'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartdetail',
            name='count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]