from django.db import models
from django.forms import IntegerField
from django.contrib.auth.models import User


class Profile(models.Model):
    age = models.IntegerField()
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Profile of {self.user.username}"
    