# Generated by Django 3.1.4 on 2020-12-12 07:59

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediator', '0008_auto_20201211_0947'),
    ]

    operations = [
        migrations.CreateModel(
            name='createPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fb_post', models.BooleanField(default=False)),
                ('fb_time', models.DateTimeField(blank=True, null=True)),
                ('ig_post', models.BooleanField(default=False)),
                ('ig_time', models.DateTimeField(blank=True, null=True)),
                ('web_post', models.BooleanField(default=False)),
                ('titulek', models.CharField(max_length=255)),
                ('text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('hashtags', models.CharField(max_length=255)),
            ],
        ),
    ]