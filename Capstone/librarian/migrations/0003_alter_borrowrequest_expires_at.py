# Generated by Django 5.0.3 on 2024-05-25 11:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0002_alter_borrowrequest_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrequest',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 28, 11, 23, 51, 754124, tzinfo=datetime.timezone.utc)),
        ),
    ]
