from django.contrib.auth.models import Group
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from librarian.models import Books

# Create your models here.
class Account(models.Model):
    lrn = models.CharField(max_length=12)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    birthday = models.DateField()
    age = models.IntegerField()
    gradeLvl = models.CharField(max_length=50, null=True)
    father = models.CharField(max_length=50)
    mother = models.CharField(max_length=50)
    guardian = models.CharField(max_length=50 ,null=True)
    semester = models.CharField(max_length=50 ,null=True)
    track = models.CharField(max_length=50 ,null=True)
    strand = models.CharField(max_length=50, null=True)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.lrn + ' ' + str(self.birthday)
    

@receiver(post_save, sender=Account)
def create_user_and_assign_to_group(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.lrn, password=str(instance.birthday))
        student_group, _ = Group.objects.get_or_create(name='Student')
        user.groups.add(student_group)


class Librarian(models.Model):
    Username = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    contactNo = models.CharField(max_length=50)
    Bday = models.DateField()

@receiver(post_save, sender=Librarian)
def create_user_and_assign_to_group(sender, instance, created, **kwargs):
    if created:
        user = User.objects.create_user(username=instance.Username, password=str(instance.Bday))
        student_group, _ = Group.objects.get_or_create(name='Librarian')
        user.groups.add(student_group)
