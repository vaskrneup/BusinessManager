from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
import datetime

# custom imports !
from shareManager.extras import NepseAPI
from .models import ShareCompanyDetail, ShareCompanyAggregate, ShareCompanyName
from users import forms as user_forms


# admin views for doing db things and other updates !
@login_required
def update_database(request):
    if not request.user.is_superuser:
        raise Http404("Link not found !")
    """
    :param request: gets request while requesting a file !
    :return: HTTPResponse for rendering as html in webpage !
    """
    # create cache for doing fetching data later !
    aggregate_cache = ShareCompanyAggregate.objects.all().last()

    # check if there is any record in database table !
    if aggregate_cache:
        # get last date !
        last_record_date = aggregate_cache.total_transaction_date
        # get date for one day after, and request data from that day to today !
        share_values = NepseAPI.get_nepse_data(str(last_record_date + datetime.timedelta(days=1)),
                                               str(datetime.date.today()))
    else:
        # just get date for very first day of share market !
        share_values = NepseAPI.get_nepse_data_for_date("2010-04-15")

    # initiate required values !
    count = 0
    first = []
    third = []

    # loop through dates provided by api !
    for date in share_values:
        # loop for each time record in every date !
        for time in share_values[date]:
            # get key for data !
            key = share_values[date][time]

            # create object of grabbed data !
            aggregate = ShareCompanyAggregate(
                total_transaction_date=date,
                total_transaction_time=time,
                total_amount=int(key["total_amount_rs"]),
                total_quantity=int(key["total_quantity"]),
                total_num_of_transactions=int(key["total_num_of_transactions"])
            )
            # append to list for batch processing !
            # aggregate.save()  --> slower method !
            first.append(aggregate)

            # get cache for all data of companies !
            cache = ShareCompanyName.objects.all()

            # loop through each company transaction in particular time in a particular date !
            for c in key["company_data"]:
                # get data for the company !
                share_company_name_cache = cache.filter(company_full_name=c[1])

                # this is not done in batch processing because it must be unique !
                # check if company exists or not !
                if share_company_name_cache.exists():
                    # get company data if company exists !
                    share_company = share_company_name_cache.first()
                else:
                    # if company doesnt exists then create one !
                    share_company = ShareCompanyName(
                        company_full_name=c[1]
                    )
                    # save the company if it doesnt exists !
                    share_company.save()
                    # sec.append(share_company)

                # create object of company detail
                company_detail = ShareCompanyDetail(
                    company_name=share_company,
                    company_transaction_date=date,
                    company_transaction_time=time,
                    company_sn=int(c[0]),
                    company_num_of_transaction=int(c[2]),
                    company_max_price=float(c[3]),
                    company_min_price=float(c[4]),
                    company_closing_price=float(c[5]),
                    company_traded_shares=float(c[6]),
                    company_total_amount=float(c[7]),
                    company_previous_closing=float(c[8]),
                    company_difference=float(c[9])
                )
                # append for batch processing !
                # company_detail.save() --> slower method !
                third.append(company_detail)
        # for knowing how many company added !
        count += 1
        print(f"Total Number of data: {count}")

    # bulk save created objects !
    ShareCompanyAggregate.objects.bulk_create(first)
    # ShareCompanyName.objects.bulk_create(sec)
    ShareCompanyDetail.objects.bulk_create(third)

    # return data for what data is grabbed !
    return HttpResponse(f"Done Something, total data grabbed: {count}<br><br><hr>Share Data:<br>{share_values}")


# END ADMIN VIEWS !


# start views for rendering dashboard pages !
@login_required
def share_manager_dashboard_home(request):
    # keeps track of data that is to be rendered in django templates !
    template_data = {
        # "title": "Dashboard",
        "current": "sm_dashboard"
    }
    return render(request, template_name="shareManager/dashboard_home.html", context=template_data)


# TODO: Transfer this to UserDashboard !
# for displaying user profile and their data !
@login_required
def share_manager_dashboard_profile(request):
    # create forms with data pre filled !
    user_update_form = user_forms.UserUpdateSettingsForm(instance=request.user)
    user_profile_update_form = user_forms.UserProfileUpdateSettingsForm(instance=request.user.userprofile)

    # for rendering data !
    template_data = {
        "user_update_form": user_update_form,
        "user_profile_update_form": user_profile_update_form,
        "current": "sm_profile",
    }

    return render(request, template_name="shareManager/dashboard_profile.html", context=template_data)
