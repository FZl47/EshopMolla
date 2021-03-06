# Generated by Django 3.2.6 on 2022-02-09 23:40

import Config.Tools
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(default=Config.Tools.RandomString, max_length=20)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('slug', models.SlugField()),
                ('datecreate', models.DateTimeField(auto_now_add=True)),
                ('dateupdate', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('deactive', 'Deactive')], default='deactive', max_length=10)),
                ('categories', models.ManyToManyField(related_name='categories', to='Product.Category')),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
