# Generated by Django 3.2.6 on 2022-02-13 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_alter_color_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color', to='Product.product'),
        ),
    ]
