from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ShareCompanyName(models.Model):
    company_full_name = models.CharField("Full Name", max_length=256, null=False, blank=False, unique=True)
    company_short_name = models.CharField("Short Name", max_length=20, null=True, blank=True, unique=True)

    def __str__(self):
        return self.company_full_name


class ShareCompanyAggregate(models.Model):
    total_transaction_date = models.DateField("Share Date", null=False, blank=False)
    total_transaction_time = models.TimeField("share Time", null=False, blank=False)

    total_amount = models.FloatField("Total Amount Rs.")
    total_quantity = models.IntegerField("Total Quantity")
    total_num_of_transactions = models.IntegerField("Total Number of Transactions")

    def __str__(self):
        return str(self.total_transaction_date)


class ShareCompanyDetail(models.Model):
    company_name = models.ForeignKey(ShareCompanyName, on_delete=models.CASCADE)

    company_transaction_date = models.DateField("Share Date", null=False, blank=False)
    company_transaction_time = models.TimeField("share Time", null=False, blank=False)

    company_sn = models.IntegerField("Daily ID", null=False, blank=False)
    company_num_of_transaction = models.IntegerField("Total Number of Transaction", null=False, blank=False)
    company_max_price = models.FloatField("Company Max Price", null=False, blank=False)
    company_min_price = models.FloatField("Company Min Price", null=False, blank=False)
    company_closing_price = models.FloatField("Company Closing Price", null=False, blank=False)
    company_traded_shares = models.IntegerField("Company Traded Shares", null=False, blank=False)
    company_total_amount = models.FloatField("Company Total Transaction Amount", null=False, blank=False)
    company_previous_closing = models.FloatField("Company Closing Price", null=False, blank=False)
    company_difference = models.FloatField("Company Difference", null=False, blank=False)

    def __str__(self):
        return str(self.company_transaction_date)


# TODO !
class ShareManagerUserDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    share_phone_number_1 = models.CharField("Phone Number 1", max_length=15)
    share_phone_number_2 = models.CharField("Phone Number 2", max_length=15)

    share_email_1 = models.CharField("email 1", max_length=15)
    share_email_2 = models.CharField("email 2", max_length=15)

    Share_address = models.CharField("Address", max_length=512)
    Share_city = models.CharField("city", max_length=256)
    Share_country = models.CharField("country", max_length=128)

    share_profile_picture = models.ImageField("Share Profile Picture", default="profilePicture/default.png",
                                              upload_to="profilePicture")

    share_dashboard_left_nav_show = models.BooleanField(default=True)
    show_notification_popup = models.BooleanField(default=True)
    show_email_popup = models.BooleanField(default=True)
    keep_activity_log = models.BooleanField(default=True)

    def __str__(self):
        return self.share_email_1


class ShareManagerUserShareValues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share_company_name = models.ForeignKey(ShareCompanyName, on_delete=models.CASCADE)

    share_bought_date = models.DateTimeField("Share Bought Date", default=timezone.datetime.now)

    share_company_bought_per_unit_price = models.FloatField("Share Per Unit Price")
    share_company_number_of_shares_bought = models.IntegerField("Number of share Bought")
    share_company_bought_total_price = models.FloatField("Total Amount", blank=True)

    current_share_count_ledger = models.IntegerField(default=0)
    current_share_amount_ledger = models.FloatField(default=0.0)

    share_company_bought_remarks = models.TextField(blank=True)
    share_company_buy = models.BooleanField(default=True)

    # calculate values for other columns !
    def update_ledger(self, instance=None):
        # gets value of ledger for last transaction !
        last_transaction = instance

        if self.share_company_buy:
            self.share_company_bought_total_price \
                = self.share_company_bought_per_unit_price * self.share_company_number_of_shares_bought
        else:
            self.share_company_bought_total_price \
                = -(self.share_company_bought_per_unit_price * self.share_company_number_of_shares_bought)

        if last_transaction:
            self.current_share_amount_ledger = \
                last_transaction.current_share_amount_ledger + self.share_company_bought_total_price

            self.current_share_count_ledger = \
                last_transaction.current_share_count_ledger + self.share_company_number_of_shares_bought

    def get_current_price(self, query_cache=None):
        cache = query_cache.filter(company_name=self.share_company_name).last()
        if cache:
            return cache.company_closing_price * self.share_company_number_of_shares_bought
        else:
            return self.share_company_number_of_shares_bought * 100

    def __str__(self):
        return f"--{self.share_company_bought_remarks}"
