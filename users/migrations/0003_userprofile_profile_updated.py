# Generated by Django 3.0.4 on 2020-03-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200327_1619'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_updated',
            field=models.BooleanField(default=False),
        ),
    ]
