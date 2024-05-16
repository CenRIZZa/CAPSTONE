# Generated by Django 5.0.3 on 2024-04-07 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0005_books_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='Language',
            field=models.CharField(choices=[('english', 'English'), ('filipino', 'Filipino'), ('spanish', 'Spanish'), ('other', 'Other')], default='english', max_length=100),
        ),
    ]
