# Generated by Django 5.0 on 2023-12-30 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogmodel_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogmodel',
            name='file',
        ),
    ]
