<<<<<<< HEAD
# Generated by Django 5.0.3 on 2024-05-24 17:15
=======
# Generated by Django 5.0.3 on 2024-05-24 18:01
>>>>>>> c7ef06bd4e11ec762da984fc2d2026204ac048c0

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ('librarian', '0003_alter_borrowrequest_expires_at'),
=======
        ('librarian', '0003_books_research_paper_alter_borrowrequest_expires_at'),
>>>>>>> c7ef06bd4e11ec762da984fc2d2026204ac048c0
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowrequest',
            name='expires_at',
<<<<<<< HEAD
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 17, 15, 50, 930394, tzinfo=datetime.timezone.utc)),
=======
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 27, 18, 1, 48, 635064, tzinfo=datetime.timezone.utc)),
>>>>>>> c7ef06bd4e11ec762da984fc2d2026204ac048c0
        ),
    ]
