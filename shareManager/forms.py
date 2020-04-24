from django import forms

from . import models as share_manager_models


class AddShareDataForm(forms.ModelForm):
    share_company_name = forms.ModelChoiceField(
        queryset=share_manager_models.ShareCompanyName.objects.order_by(
            'company_full_name'
        )
    )

    class Meta:
        model = share_manager_models.ShareManagerUserShareValues
        fields = (
            "share_company_name", "share_company_bought_per_unit_price",
            "share_company_number_of_shares_bought", "share_company_bought_remarks",
            "share_company_buy"
        )
        labels = {
            "share_company_name": "Company Name",
            "share_company_bought_per_unit_price": "Cost Per Unit Price",
            "share_company_number_of_shares_bought": "Number of Share",
            "share_company_bought_remarks": "Remarks",
            "share_company_buy": "TICK for buying, UN-TICK for selling"
        }

    def clean_share_company_bought_per_unit_price(self):
        x = self.cleaned_data["share_company_bought_per_unit_price"]
        if x < 0:
            raise forms.ValidationError("Please give positive value !")

        return x


class ShareCompanyForm(forms.Form):
    share_company_name = forms.ModelChoiceField(
        queryset=share_manager_models.ShareCompanyName.objects.order_by(
            'company_full_name'
        ),
        required=True
    )


class ShareInvestmentCheckForm(forms.Form):
    share_company_name = forms.ModelChoiceField(
        queryset=share_manager_models.ShareCompanyName.objects.order_by(
            'company_full_name'
        ),
        required=True
    )

    date = forms.DateField(widget=forms.SelectDateWidget(years=[y for y in range(2010, 2021)]))

    number_of_share = forms.IntegerField(required=True)
    # per_unit_price = forms.FloatField(required=True)


class ShareInvestmentResultForm(forms.Form):
    given_date_price = forms.FloatField(required=False)
    todays_price = forms.FloatField(required=False)
    last_date_price = forms.FloatField(required=False)

    given_date_value = forms.FloatField(required=False)
    todays_value = forms.FloatField(required=False)
    last_date_value = forms.FloatField(required=False)

    profit_or_loss = forms.FloatField(required=False)
