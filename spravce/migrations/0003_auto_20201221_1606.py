# Generated by Django 3.1.4 on 2020-12-21 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('spravce', '0002_auto_20201221_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clenstvi',
            name='skupina',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='spravce.skupina'),
        ),
        migrations.AlterField(
            model_name='clenstvi',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]