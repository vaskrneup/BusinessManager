from django.urls import path

from . import views as user_views

# specify app name for making it easier to work with multiple app !
app_name = "users"

urlpatterns = [
    # Admin URLS !

    # Users URLS !
    # rendering for authenticated users !
    path("logout/", user_views.user_logout, name="user_logout"),
    path("dashboard/", user_views.user_dashboard, name="user_dashboard"),
    path("profile/", user_views.user_profile, name="user_profile"),

    # rendering for unauthenticated users !
    path("login/", user_views.user_login, name="user_login"),
    path("register/", user_views.user_register, name="user_register"),
    path("reset-password/", user_views.user_password_reset, name="user_password_reset"),
]
