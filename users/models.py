# inbuilt uploads !
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# custom imports !
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_identification_card_picture_front = models.ImageField('Identification Card Front',
                                                               upload_to="userIdentificationCard",
                                                               blank=True, null=True)
    user_identification_card_picture_back = models.ImageField('Identification Card Back',
                                                              upload_to="userIdentificationCard",
                                                              blank=True, null=True)
    user_identification_card_number = models.CharField('Identification Card Number', max_length=30,
                                                       blank=True, null=True, unique=True)
    user_date_of_birth = models.DateField('Date of Birth', blank=True, null=True)

    user_profile_picture = models.ImageField('User Passport Size Photo', upload_to="profilePicture",
                                             blank=True, null=True)

    user_phone_number = models.CharField('Phone Number',
                                         help_text="Only Nepalese number available for now, Format: 98XXXXXXXX",
                                         max_length=10, validators=[MinLengthValidator(10)], unique=True)

    @property
    def get_user_full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return f"{self.user.username} profile picture !"
