# Generated by Django 3.2.6 on 2022-02-22 03:37

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Public', '0005_auto_20220222_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='contact_information',
            field=ckeditor.fields.RichTextField(default='ad'),
            preserve_default=False,
        ),
    ]