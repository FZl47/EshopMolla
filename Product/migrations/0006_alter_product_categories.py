# Generated by Django 3.2.6 on 2022-02-10 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_alter_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(related_name='product', to='Product.Category'),
        ),
    ]
