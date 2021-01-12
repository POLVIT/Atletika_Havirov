from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User=get_user_model()

class Vykazy(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date=models.DateField()
    udalost=models.TextField(max_length=100)
    popis=models.TextField(max_length=255)