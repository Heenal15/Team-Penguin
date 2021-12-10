# Generated by Django 3.2.5 on 2021-12-08 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_alter_user_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='clubs',
            field=models.CharField(default='Kerbal', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='beginner', max_length=20),
        ),
    ]
