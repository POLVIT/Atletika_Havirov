# Generated by Django 3.1.4 on 2020-12-12 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediator', '0011_createpost_foto_urls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createpost',
            name='titulek',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
