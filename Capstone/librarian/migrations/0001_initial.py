# Generated by Django 5.0.3 on 2024-05-23 20:02

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Def', max_length=100)),
                ('code', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BookTitle', models.CharField(max_length=100)),
                ('Author', models.CharField(max_length=100)),
                ('Description', models.TextField(blank=True, null=True)),
                ('Date', models.DateField()),
                ('Language', models.CharField(choices=[('english', 'English'), ('filipino', 'Filipino'), ('spanish', 'Spanish'), ('other', 'Other')], default='english', max_length=100)),
                ('BookFile', models.FileField(default='default_value.pdf', upload_to='books/files/')),
                ('BookImage', models.ImageField(default='default_image.jpg', upload_to='books/images/')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
                ('PageViews', models.IntegerField(default=0)),
                ('eBook', models.BooleanField(default=False)),
                ('hardCopy', models.BooleanField(default=False)),
                ('stock', models.IntegerField(default=0)),
                ('bookmarked_by', models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
                ('borrowed', models.ManyToManyField(blank='True', related_name='borrow', to=settings.AUTH_USER_MODEL)),
                ('Category', models.ManyToManyField(to='librarian.category')),
            ],
        ),
        migrations.CreateModel(
            name='ApprovedRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField()),
                ('approved_at', models.DateTimeField(auto_now_add=True)),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarian.books')),
            ],
        ),
        migrations.CreateModel(
            name='BorrowRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(default=datetime.datetime(2024, 5, 26, 20, 2, 43, 899496, tzinfo=datetime.timezone.utc))),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Expired', 'Expired')], default='Pending', max_length=20)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarian.books')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeclinedRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_at', models.DateTimeField()),
                ('declined_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='librarian.books')),
                ('requested_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
