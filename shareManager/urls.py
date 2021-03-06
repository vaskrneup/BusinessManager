from django.urls import path

from . import views as share_manager_views

# specify app name for making it easier to work with multiple app !
app_name = "shareManager"

urlpatterns = [
    # Admin URLS !
    path("update-database/", share_manager_views.update_database, name="update_database"),

    # Users URLS !
    # rendering for authenticated users !
    path("dashboard/", share_manager_views.share_manager_dashboard_home, name="dashboard_home"),
    path("profile/", share_manager_views.share_manager_dashboard_profile, name="dashboard_profile"),
    path("add-share-data/", share_manager_views.add_share_data, name="add_share_data"),
    path("share-transaction-ledger/", share_manager_views.user_share_ledger, name="show_share_ledger"),
    path("share-price-history/", share_manager_views.share_price_history, name="show_share_history"),
    path("share-price-history-graphical-view/", share_manager_views.share_price_history_graphical_view,
         name="show_share_history_graphical_view"),
    path("share-price-history-graphical-view-for-company/",
         share_manager_views.show_price_history_graphical_view_for_particular_company,
         name="share_company_graphical_view_for_particular_company"),
    path("share-value-check-form/", share_manager_views.investment_checker,
         name="share_company_investment_check")
    # rendering for unauthenticated users !

]
