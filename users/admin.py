from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user']}),
        ('User Identification Data', {
            'fields': ['user_identification_card_picture_front', "user_identification_card_picture_back",
                       "user_profile_picture", "user_identification_card_number", "user_date_of_birth"]
        }),
        ('User Contact Details', {
            "fields": ["user_phone_number"]
        })
    ]
    list_display = ("get_user_full_name", "user_identification_card_number", "user_phone_number")


admin.site.register(UserProfile, UserProfileAdmin)
