# Generated by Django 3.2.5 on 2021-12-10 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0007_merge_20211210_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='clubs',
        ),
    ]
