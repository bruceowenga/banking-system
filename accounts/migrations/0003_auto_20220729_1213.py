# Generated by Django 3.1.8 on 2022-07-29 09:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_meeting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='user',
        ),
        migrations.AddField(
            model_name='meeting',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='meetings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meeting',
            name='meeting_name',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
