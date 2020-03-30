# inbuilt imports !
from django import forms
from django.contrib.auth.models import User

# custom imports !
from .models import UserProfile, UserGlobalSettings


# For Local Form !
# For logging in the user !
class UserLoginForm(forms.Form):
    # just create forms for keeping data and validation !
    username = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(max_length=80, required=True, widget=forms.PasswordInput())


# for registering user !
class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput())

    class Meta:
        model = User
        # just provide some fields !
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirm_password')

    # change how default models are designed !
    def __init__(self, *args, **kwargs):
        # call the main init function !
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # make field display text as password !
        self.fields["password"].widget = forms.PasswordInput()
        self.fields["password"].min_length = 8
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    def clean_email(self):
        # check if email is already taken !
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken.")

        return email

    def clean(self):
        # call main clean method !
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # check if password field are non empty !
        if password and confirm_password:
            if password != confirm_password:
                self.add_error("password", "passwords didn't match.")
                self.add_error("confirm_password", "passwords didn't match.")
            elif len(password) < 8 or len(password) > 32:
                self.add_error("password", "Password must be of length between 8 and 32.")
                self.add_error("confirm_password", "Password must be of length between 8 and 32.")


# for registering user profile with basic info !
class UserProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_profile_picture', 'user_phone_number')


# For Global Form !
# For Updating User model data !
class UserUpdateSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username")

    # change how default models are designed !
    def __init__(self, *args, **kwargs):
        # call the main init function !
        super(UserUpdateSettingsForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["username"].help_text = None


# For updating UserProfile model data !
class UserProfileUpdateSettingsForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "user_identification_card_picture_front", "user_identification_card_picture_back",
            "user_identification_card_number", "user_date_of_birth"
        )

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateSettingsForm, self).__init__(*args, **kwargs)
        self.fields["user_identification_card_picture_front"].required = True
        self.fields["user_identification_card_picture_back"].required = True
        self.fields["user_identification_card_number"].required = True
        self.fields["user_date_of_birth"].required = True


# for updating user profile picture !
class UserProfilePictureUpdateForm(forms.ModelForm):
    user_profile_picture = forms.ImageField(required=True)

    class Meta:
        model = UserProfile
        fields = ("user_profile_picture",)


class UserGlobalSettingsUpdateForm(forms.ModelForm):
    class Meta:
        model = UserGlobalSettings
        fields = ("user_address", "user_city", "user_country")


class UserGlobalSettingsUpdateEmailForm(forms.ModelForm):
    user_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, req_data: User, **kwargs):
        super().__init__(*args, **kwargs)
        self.req_data = req_data

        self.fields["email"].required = True

    def clean_user_password(self):
        if not self.req_data.user.check_password(self.cleaned_data['user_password']):
            raise forms.ValidationError("Incorrect Password !")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists() and self.req_data.user.email != email:
            raise forms.ValidationError("Email Already in use !")


class UserGlobalSettingsUpdatePhoneNumberForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("user_phone_number",)
