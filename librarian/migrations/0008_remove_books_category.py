# Generated by Django 5.0.3 on 2024-04-07 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0007_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='Category',
        ),
    ]
