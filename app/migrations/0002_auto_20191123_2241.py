# Generated by Django 2.2 on 2019-11-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcements',
            name='end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='announcements',
            name='start',
            field=models.DateField(null=True),
        ),
    ]