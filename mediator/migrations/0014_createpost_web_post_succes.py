# Generated by Django 3.1.4 on 2020-12-16 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediator', '0013_auto_20201213_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='createpost',
            name='web_post_succes',
            field=models.BooleanField(default=False),
        ),
    ]