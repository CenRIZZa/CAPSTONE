# Generated by Django 5.0.3 on 2024-04-07 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('librarian', '0008_remove_books_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='Categories',
            field=models.ManyToManyField(to='librarian.category'),
        ),
    ]
