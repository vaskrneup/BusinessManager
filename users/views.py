from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate as authenticate_user, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from . import forms as user_forms


# for registering user !
def user_register(request):
    # check if request is post or not !
    if request.method == "POST":
        # create form with filled data !
        user_profile_form = user_forms.UserProfileRegistrationForm(request.POST, request.FILES)
        user_register_form = user_forms.UserRegisterForm(request.POST)

        # check if form is valid or not !
        if user_register_form.is_valid() and user_profile_form.is_valid():
            # save user form grabbing the model it created !
            form_user = user_register_form.save(commit=False)
            # create hash for user password !
            form_user.set_password(user_register_form.cleaned_data["password"])
            # save user !
            form_user.save()

            # get user profile model without saving to database !
            form_user_profile = user_profile_form.save(commit=False)
            # provide the user who is related to this profile !
            form_user_profile.user = form_user
            # save the profile !
            form_user_profile.save()

            # create default settings configuration for user !
            form_user_profile.create_default_settings()

            # login the user !
            login(request, form_user)
            # display message !
            messages.info(request, "You are now logged in !")
            # TODO: This must be changed to main profile !
            return redirect('users:user_profile')
    else:
        # create empty form !
        user_register_form = user_forms.UserRegisterForm()
        user_profile_form = user_forms.UserProfileRegistrationForm()

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
        user_login_form = user_forms.UserLoginForm(request.POST)

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

            # check if verified !
            if current_user:
                # login using authenticated data !
                login(request, current_user)
                # redirect to dashboard homepage !
                return redirect('users:user_dashboard')
            else:
                # if invalid data is provided then flash the message !
                messages.warning(request, 'Your username/email or password is incorrect !')
    # the request is get (at least right now) !
    else:
        # create new user form !
        user_login_form = user_forms.UserLoginForm()

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


# for user dashboard !
@login_required
def user_dashboard(request):
    # keeps track of data that is to be rendered in django templates !
    template_data = {
        # "title": "Dashboard",
        "current": "dashboard",
        "current_for": "user",

    }
    return render(request, template_name="shareManager/dashboard_home.html", context=template_data)


# TODO: Transfer this to UserDashboard !
# for displaying user profile and their data !
@login_required
def user_profile(request):
    # create forms with data pre filled !
    # define at first because post have many forms !
    user_update_form = user_forms.UserUpdateSettingsForm(instance=request.user)
    user_profile_update_form = user_forms.UserProfileUpdateSettingsForm(instance=request.user.userprofile)

    # for updating profile picture !
    user_profile_pic_update_form = user_forms.UserProfilePictureUpdateForm()

    # for updating user contact info !
    user_contact_details_update_form = user_forms.UserGlobalSettingsUpdateForm(
        instance=request.user.userglobalsettings)
    user_email_update_form = user_forms.UserGlobalSettingsUpdateEmailForm(instance=request.user, req_data=request)
    user_phone_number_update_form = user_forms.UserGlobalSettingsUpdatePhoneNumberForm(
        instance=request.user.userprofile)

    # data is submitted to form !
    if request.method == "POST":
        print(request.FILES)
        print(request.POST)
        if "user_identification_card_number" in request.POST:
            user_update_form = user_forms.UserUpdateSettingsForm(request.POST, instance=request.user)
            user_profile_update_form = user_forms.UserProfileUpdateSettingsForm(request.POST, request.FILES,
                                                                                instance=request.user.userprofile)

            if user_update_form.is_valid() and user_profile_update_form.is_valid():
                if request.user.userprofile.can_update_profile():
                    user_update_form.save()
                    user_profile = user_profile_update_form.save(commit=False)
                    user_profile.profile_updated = True
                    user_profile.save()
                    messages.info(request, "Your data is updated successfully !")
                else:
                    messages.warning(request, "You have already updated profile once !")
                return redirect("users:user_dashboard")
            else:
                messages.info(request, "Please provide valid data !")

        elif "user_profile_picture" in request.FILES:
            user_profile_pic_update_form = user_forms.UserProfilePictureUpdateForm(request.POST, request.FILES,
                                                                                   instance=request.user.userprofile)

            if user_profile_pic_update_form.is_valid():
                user_profile_pic_update_form.save()

        elif "user_address" in request.POST:
            user_contact_details_update_form = user_forms.UserGlobalSettingsUpdateForm(
                request.POST, instance=request.user.userglobalsettings
            )
            user_phone_number_update_form = user_forms.UserGlobalSettingsUpdatePhoneNumberForm(
                request.POST, instance=request.user.userprofile
            )
            user_email_update_form = user_forms.UserGlobalSettingsUpdateEmailForm(
                request.POST, req_data=request, instance=request.user
            )

            if user_contact_details_update_form.is_valid() and user_email_update_form.is_valid() and \
                    user_phone_number_update_form.is_valid():
                user_contact_details_update_form.save()
                user_phone_number_update_form.save()
                user_email_update_form.save()
                messages.info(request, "Contact info updated !")

    # for rendering data !
    template_data = {
        "user_update_form": user_update_form,
        "user_profile_update_form": user_profile_update_form,
        "user_profile_pic_update_form": user_profile_pic_update_form,
        "user_contact_details_update_form": user_contact_details_update_form,
        "user_email_update_form": user_email_update_form,
        "user_phone_number_update_form": user_phone_number_update_form,
        "current": "profile",
        "current_for": "user",
    }
    
    return render(request, template_name="users/dashboard_profile.html", context=template_data)
