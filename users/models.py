# inbuilt uploads !
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models

# custom imports !
from shareManager import models as share_manager_models


# TODO !
class UserGlobalSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_address = models.CharField("Address", max_length=512)
    user_city = models.CharField("city", max_length=256)
    user_country = models.CharField("country", max_length=128)

    def __str__(self):
        return self.user_address


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
                                             blank=True, null=True, default="profilePicture/default.png")

    user_phone_number = models.CharField('Phone Number',
                                         help_text="Only Nepalese number available for now, Format: 98XXXXXXXX",
                                         max_length=10, validators=[MinLengthValidator(10)], unique=True)

    profile_updated = models.BooleanField(default=False)

    def create_default_settings(self):
        # create default user settings for this guy !
        UserGlobalSettings(user=self.user).save()
        share_manager_models.ShareManagerLedger(user=self.user).save()

    @property
    def get_user_full_name(self):
        return self.user.get_full_name()

    def can_update_profile(self):
        return not self.profile_updated

    def __str__(self):
        return f"{self.user.username} profile picture !"
