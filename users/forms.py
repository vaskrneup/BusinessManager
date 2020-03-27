# inbuilt imports !
from django import forms
from django.contrib.auth.models import User

# custom imports !
from .models import UserProfile


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(max_length=80, required=True, widget=forms.PasswordInput())


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=80, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email Already Taken !")

    def clean_password(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("confirm_password"):
            raise forms.ValidationError("Passwords didn't match !")


class UserProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_profile_picture', 'user_phone_number')

    def clean_user_phone_number(self):
        # TODO: Complete this !
        pass
