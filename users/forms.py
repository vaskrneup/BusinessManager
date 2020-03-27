# inbuilt imports !
from django import forms
from django.contrib.auth.models import User

# custom imports !
from .models import UserProfile


# For Local Form !
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(max_length=80, required=True, widget=forms.PasswordInput())


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields["password"].widget = forms.PasswordInput()
        self.fields["password"].min_length = 8
        self.fields["first_name"].required = True
        self.fields["last_name"].required = True
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already taken.")

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error("password", "passwords didn't match.")
                self.add_error("confirm_password", "passwords didn't match.")
            elif len(password) < 8 or len(password) > 32:
                self.add_error("password", "Password must be of length between 8 and 32.")
                self.add_error("confirm_password", "Password must be of length between 8 and 32.")


class UserProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_profile_picture', 'user_phone_number')
