# Generated by Django 3.1.4 on 2020-12-05 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OsobniInformace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jmeno', models.CharField(max_length=30)),
                ('prijmeni', models.CharField(max_length=30)),
                ('rodne_cislo', models.CharField(max_length=10, unique=True)),
                ('datum_narozeni', models.DateField()),
                ('mesto', models.CharField(max_length=50)),
                ('ulice', models.CharField(max_length=100)),
                ('psc', models.CharField(max_length=5)),
                ('telefon', models.CharField(max_length=9)),
                ('email', models.EmailField(max_length=254)),
                ('gdpr', models.ImageField(default=None, upload_to='gdpr')),
                ('lekarske_potvrzeni', models.ImageField(default=None, upload_to='doktor')),
                ('prispevky', models.BooleanField(default=False)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]