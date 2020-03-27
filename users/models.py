# inbuilt uploads !
from django.contrib.auth.models import User

# custom imports !
from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    user_profile_picture = models.ImageField('Profile Picture', upload_to="profilePicture")
    user_phone_number = models.CharField('Phone Number', max_length=15)

    def __str__(self):
        return f"{self.user.username} profile picture !"
