# Generated by Django 3.2.6 on 2022-02-22 03:16

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Public', '0004_outstor_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteinfo',
            name='our_mission',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='siteinfo',
            name='our_vision',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
