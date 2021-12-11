# Generated by Django 3.2.5 on 2021-12-10 17:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0004_alter_user_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.PositiveSmallIntegerField(choices=[(0, 'Applicant'), (1, 'Member'), (2, 'Club Officer'), (3, 'Club Owner')], primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='experience',
            field=models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')], default='beginner', max_length=20),
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_type',
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('club_name', models.CharField(max_length=50)),
                ('club_location', models.CharField(max_length=100)),
                ('club_description', models.CharField(max_length=520)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.ManyToManyField(to='clubs.Role'),
        ),
    ]
