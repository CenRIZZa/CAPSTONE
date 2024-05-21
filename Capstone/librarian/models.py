import os
from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.

from django.db import models
#from userauth.models import Account  # Import your custom Account model
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# Create your models here.



LANGUAGE_CHOICES = [
    ('english', 'English'),
    ('filipino', 'Filipino'),
    ('spanish', 'Spanish'),
    ('other', 'Other'),
]

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Books(models.Model):
    BookTitle = models.CharField(max_length=100)
    Author = models.CharField(max_length=100)
    Description = models.TextField(null=True, blank=True)
    Date = models.DateField()
    Category = models.ManyToManyField(Category)
    Language = models.CharField(max_length=100, choices=LANGUAGE_CHOICES, default='english')
    
    BookFile = models.FileField(upload_to="books/files/", default='default_value.pdf')
    BookImage = models.ImageField(upload_to="books/images/", default='default_image.jpg')
    deleted_at = models.DateTimeField(null=True, blank=True)
    available = models.BooleanField(default=True)
    bookmarked_by = models.ManyToManyField(User, related_name='bookmarks', blank=True)
    borrowed = models.ManyToManyField(User, related_name='borrow', blank="True")
    PageViews = models.IntegerField(default=0)

    def __str__(self):
        return self.BookTitle + ', ' + self.Author
    
class BorrowRequest(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=3))
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Denied', 'Denied'), ('Expired', 'Expired')], default='Pending')
    
    def is_expired(self):
        return timezone.now() > self.expires_at




class ApprovedRequest(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField()
    approved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book} approved for {self.requested_by}"

class DeclinedRequest(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField()
    declined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book} declined for {self.requested_by}"