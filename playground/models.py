import os
import uuid
from django.conf import settings
from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

class Brgy(models.Model):
    Barangay = models.CharField(max_length=100)

    def __str__(self):
        return self.Barangay

       





