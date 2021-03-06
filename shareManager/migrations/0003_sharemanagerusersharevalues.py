# Generated by Django 3.0.4 on 2020-03-30 16:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shareManager', '0002_sharemanageruserdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareManagerUserShareValues',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('share_company_bought_per_unit_price', models.FloatField()),
                ('share_company_number_of_shares_bought', models.PositiveIntegerField()),
                ('share_company_bought_total_price', models.FloatField(blank=True)),
                ('share_company_bought_remarks', models.TextField(blank=True)),
                ('share_company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shareManager.ShareCompanyName')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
