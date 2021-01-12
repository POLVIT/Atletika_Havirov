from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.

class OsobniInformace(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jmeno = models.CharField(max_length=30)
    prijmeni = models.CharField(max_length=30)
    rodne_cislo = models.CharField(max_length=10, unique=True)
    datum_narozeni = models.DateField()
    mesto = models.CharField(max_length=50)
    ulice = models.CharField(max_length=100)
    psc = models.CharField(max_length=5)
    telefon = models.CharField(max_length=9)
    Email = models.EmailField()
    gdpr = models.ImageField(default=None, upload_to='gdpr', blank=True, null=True)
    lekarske_potvrzeni = models.ImageField(default=None, upload_to='doktor', blank=True, null=True)
    datum_vystaveni_lekarskeho_potvrzeni = models.DateField(blank=True, null=True)
    prispevky = models.BooleanField(default=False)
    je_zkontrolovan = models.BooleanField(default=False)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return f'{self.jmeno} {self.prijmeni}'



    class Meta:
        permissions=(
            ('Mediátor','Mediátor'),
            ('Správce', 'Správce'),
        )