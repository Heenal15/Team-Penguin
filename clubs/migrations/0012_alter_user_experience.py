# Generated by Django 3.2.5 on 2021-12-11 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0011_merge_20211211_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='Beginner', max_length=20),
        ),
    ]
