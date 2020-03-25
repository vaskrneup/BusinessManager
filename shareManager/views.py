from django.shortcuts import render
from django.http import HttpResponse
import datetime

# custom imports !
from shareManager.extras import NepseAPI
from .models import ShareCompanyDetail, ShareCompanyAggregate, ShareCompanyName


def update_database(request):
    aggregate_cache = ShareCompanyAggregate.objects.all().last()

    if aggregate_cache:
        last_record_date = aggregate_cache.total_transaction_date
        share_values = NepseAPI.get_nepse_data(str(last_record_date + datetime.timedelta(days=1)), "2011-04-15")
    else:
        share_values = NepseAPI.get_nepse_data_for_date("2010-04-15")

    for date in share_values:
        for time in share_values[date]:
            key = share_values[date][time]

            aggregate = ShareCompanyAggregate(
                total_transaction_date=date,
                total_transaction_time=time,
                total_amount=int(key["total_amount_rs"]),
                total_quantity=int(key["total_quantity"]),
                total_num_of_transactions=int(key["total_num_of_transactions"])
            )
            aggregate.save()

            for c in key["company_data"]:
                share_company_name_cache = ShareCompanyName.objects.filter(company_full_name=c[1])

                if share_company_name_cache.exists():
                    share_company = share_company_name_cache.first()
                else:
                    share_company = ShareCompanyName(
                        company_full_name=c[1]
                    )
                    share_company.save()

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
                company_detail.save()
    return HttpResponse("Done Something !")
