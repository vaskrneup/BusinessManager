from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# for registering user !
@login_required
def user_register(request):
    # for rendering data !
    template_data = {
        "title": "User Register"
    }

    return render(request, template_name="users/user_register.html", context=template_data)


# for logging in user !
@login_required
def user_login(request):
    # for rendering data !
    template_data = {
        "title": "User Login"
    }

    return render(request, template_name="users/user_login.html", context=template_data)


# for resetting user password !
@login_required
def user_password_reset(request):
    # for rendering data !
    template_data = {
        "title": "Reset Password"
    }

    return render(request, template_name="users/forgot_password.html", context=template_data)
