# Generated by Django 5.0.3 on 2024-05-25 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrequest',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 28, 13, 56, 26, 417148, tzinfo=datetime.timezone.utc)),
        ),
    ]
