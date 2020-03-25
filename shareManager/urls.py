from django.urls import path

from . import views as share_manager_views

# specify app name for making it easier to work with multiple app !
app_name = "shareManager"

urlpatterns = [
    path("update-database/", share_manager_views.update_database, name="update_database"),

]
