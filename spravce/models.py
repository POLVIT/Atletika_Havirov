from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()
class Skupina(models.Model):
    nazev = models.CharField(max_length=255,blank=True,null=True)
    clenove=models.ManyToManyField(User, through='Clenstvi', blank=True,)

    def __str__(self):
        return self.nazev

class Clenstvi(models.Model):
    skupina=models.ForeignKey(Skupina, on_delete=models.CASCADE, null=True, blank=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    prava=models.BooleanField(default=False)

    class Meta:
        unique_together = ('skupina', 'user')

class Kalendar(models.Model):
    date=models.DateField(default=None)
    popisek=models.CharField(max_length=1000)
