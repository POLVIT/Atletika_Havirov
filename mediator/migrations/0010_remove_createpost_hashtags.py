# Generated by Django 3.1.4 on 2020-12-12 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mediator', '0009_createpost'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createpost',
            name='hashtags',
        ),
    ]
