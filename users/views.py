from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as authenticate_user, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from . import forms


# for registering user !
def user_register(request):
    # check if request is post or not !
    if request.method == "POST":
        # create form with filled data !
        user_profile_form = forms.UserProfileRegistrationForm(request.POST, request.FILES)
        user_register_form = forms.UserRegisterForm(request.POST)

        # check if form is valid or not !
        if user_register_form.is_valid() and user_profile_form.is_valid():
            # save user form grabbing the model it created !
            form_user = user_register_form.save()

            # get user profile model without saving to database !
            form_user_profile = user_profile_form.save(commit=False)
            # provide the user who is related to this profile !
            form_user_profile.user = form_user
            # save the profile !
            form_user_profile.save()

            # login the user !
            login(request, form_user)
            # display message !
            messages.info(request, "You are now logged in !")
            # TODO: This must be changed to main profile !
            return redirect('shareManager:dashboard_profile')
    else:
        # create empty form !
        user_register_form = forms.UserRegisterForm()
        user_profile_form = forms.UserProfileRegistrationForm()

    # for rendering data !
    template_data = {
        "user_register_form": user_register_form,
        "user_profile_form": user_profile_form,
        "title": "User Register",
    }

    return render(request, template_name="users/user_register.html", context=template_data)


# for logging in user !
def user_login(request):
    # check if user is already authenticated !
    if request.user.is_authenticated:
        # provide message !
        messages.info(request, "You need to logout before logging in to another account !")
        # TODO: Change this to other dashboard !
        # redirect to main dashboard !
        return redirect('shareManager:dashboard_home')

    # check if request is post or not !
    if request.method == "POST":
        # load form with grabbed data !
        user_login_form = forms.UserLoginForm(request.POST)

        # check if submitted data is valid or not !
        if user_login_form.is_valid():
            # grab username/email and password !
            username_or_email = user_login_form.cleaned_data['username']
            password = user_login_form.cleaned_data['password']

            # confirm it is email !
            # authenticate using email !
            if "@" in username_or_email:
                # grab user model from email !
                _user = User.objects.filter(email=username_or_email).first()
                # check if email exists in db !
                if _user:
                    # try to authenticate user !
                    current_user = authenticate_user(
                        # grab username from user model !
                        username=_user.username,
                        password=password
                    )
                    if not current_user.is_active:
                        current_user = None
                else:
                    # if email doesnt exists no current user !
                    current_user = None
            # if not email then it is username !
            else:
                # authenticate using username !
                current_user = authenticate_user(
                    request, username=username_or_email, password=password
                )
                if not current_user.is_active:
                    current_user = None

            # check if verified !
            if current_user:
                # login using authenticated data !
                login(request, current_user)
                # redirect to dashboard homepage !
                return redirect('shareManager:dashboard_home')
            else:
                # if invalid data is provided then flash the message !
                messages.warning(request, 'Your username/email or password is incorrect !')
    # the request is get (at least right now) !
    else:
        # create new user form !
        user_login_form = forms.UserLoginForm()

    # for rendering data !
    template_data = {
        "title": "User Login",
        "user_login_form": user_login_form,
    }

    return render(request, template_name="users/user_login.html", context=template_data)


# for logging out user !
def user_logout(request):
    # check if user is authenticated !
    if request.user.is_authenticated:
        # logout the user !!
        logout(request)
        # TODO: redirect to home page later !
        return redirect('users:user_login')
    else:
        return redirect('users:user_login')


# for resetting user password !
def user_password_reset(request):
    # for rendering data !
    template_data = {
        "title": "Reset Password"
    }

    return render(request, template_name="users/forgot_password.html", context=template_data)
