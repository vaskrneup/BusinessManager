from django.urls import path

from . import views as share_manager_views

# specify app name for making it easier to work with multiple app !
app_name = "shareManager"

urlpatterns = [
    # Admin URLS !
    path("update-database/", share_manager_views.update_database, name="update_database"),

    # Users URLS !
    path("dashboard/", share_manager_views.dashboard_home, name="dashboard_home")
]
