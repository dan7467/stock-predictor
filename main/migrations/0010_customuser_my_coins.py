# Generated by Django 5.1.3 on 2024-12-17 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_cryptocoinnames'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='my_coins',
            field=models.JSONField(default=list),
        ),
    ]
