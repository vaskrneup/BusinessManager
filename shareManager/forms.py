from django import forms

from . import models as share_manager_models


class AddShareDataForm(forms.ModelForm):
    class Meta:
        model = share_manager_models.ShareManagerUserShareValues
        fields = (
            "share_company_name", "share_company_bought_per_unit_price",
            "share_company_number_of_shares_bought", "share_company_bought_remarks",
            "share_company_buy_or_sell"
        )
        labels = {
            "share_company_name": "Company Name",
            "share_company_bought_per_unit_price": "Cost Per Unit Price",
            "share_company_number_of_shares_bought": "Number of Share",
            "share_company_bought_remarks": "Remarks",
            "share_company_buy_or_sell": "TICK for buying, UN-TICK for selling"
        }

    def clean_share_company_bought_per_unit_price(self):
        x = self.cleaned_data["share_company_bought_per_unit_price"]
        if x < 0:
            raise forms.ValidationError("Please give positive value !")

        return x
