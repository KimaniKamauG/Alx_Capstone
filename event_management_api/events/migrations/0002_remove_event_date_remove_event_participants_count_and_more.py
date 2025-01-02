# Generated by Django 5.1.3 on 2025-01-01 07:57

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='participants_count',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='attending_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2025, 1, 1, 7, 57, 5, 632478, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(default=datetime.datetime(2025, 1, 1, 7, 57, 31, 708795, tzinfo=datetime.timezone.utc), on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 1, 1, 7, 57, 45, 287552, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
    ]
