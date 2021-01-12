# Generated by Django 3.1.4 on 2020-12-08 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mediator', '0004_auto_20201207_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prispevekpromediatora',
            name='file',
        ),
        migrations.CreateModel(
            name='PrispevekFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='prispevky/')),
                ('prispevek', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mediator.prispevekpromediatora')),
            ],
        ),
    ]
