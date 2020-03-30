# Generated by Django 3.0.4 on 2020-03-30 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile_profile_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_profile_picture',
            field=models.ImageField(blank=True, default='profilePicture/default.png', null=True, upload_to='profilePicture', verbose_name='User Passport Size Photo'),
        ),
    ]
