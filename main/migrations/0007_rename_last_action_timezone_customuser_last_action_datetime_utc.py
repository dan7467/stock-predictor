# Generated by Django 5.1.3 on 2024-12-10 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_customuser_last_action_timezone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='last_action_timezone',
            new_name='last_action_datetime_utc',
        ),
    ]
