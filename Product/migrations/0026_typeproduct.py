# Generated by Django 3.2.6 on 2022-02-15 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0025_cartdetail_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
    ]
