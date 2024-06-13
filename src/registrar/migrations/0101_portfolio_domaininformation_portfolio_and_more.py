# Generated by Django 4.2.10 on 2024-06-12 23:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import registrar.models.portfolio


class Migration(migrations.Migration):

    dependencies = [
        ("registrar", "0100_domainrequest_action_needed_reason"),
    ]

    operations = [
        migrations.CreateModel(
            name="Portfolio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "organization_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("federal", "Federal"),
                            ("interstate", "Interstate"),
                            ("state_or_territory", "State or territory"),
                            ("tribal", "Tribal"),
                            ("county", "County"),
                            ("city", "City"),
                            ("special_district", "Special district"),
                            ("school_district", "School district"),
                        ],
                        help_text="Type of organization",
                        max_length=255,
                        null=True,
                    ),
                ),
                ("organization_name", models.CharField(blank=True, null=True)),
                ("address_line1", models.CharField(blank=True, null=True, verbose_name="address line 1")),
                ("address_line2", models.CharField(blank=True, null=True, verbose_name="address line 2")),
                ("city", models.CharField(blank=True, null=True)),
                (
                    "state_territory",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("AL", "Alabama (AL)"),
                            ("AK", "Alaska (AK)"),
                            ("AS", "American Samoa (AS)"),
                            ("AZ", "Arizona (AZ)"),
                            ("AR", "Arkansas (AR)"),
                            ("CA", "California (CA)"),
                            ("CO", "Colorado (CO)"),
                            ("CT", "Connecticut (CT)"),
                            ("DE", "Delaware (DE)"),
                            ("DC", "District of Columbia (DC)"),
                            ("FL", "Florida (FL)"),
                            ("GA", "Georgia (GA)"),
                            ("GU", "Guam (GU)"),
                            ("HI", "Hawaii (HI)"),
                            ("ID", "Idaho (ID)"),
                            ("IL", "Illinois (IL)"),
                            ("IN", "Indiana (IN)"),
                            ("IA", "Iowa (IA)"),
                            ("KS", "Kansas (KS)"),
                            ("KY", "Kentucky (KY)"),
                            ("LA", "Louisiana (LA)"),
                            ("ME", "Maine (ME)"),
                            ("MD", "Maryland (MD)"),
                            ("MA", "Massachusetts (MA)"),
                            ("MI", "Michigan (MI)"),
                            ("MN", "Minnesota (MN)"),
                            ("MS", "Mississippi (MS)"),
                            ("MO", "Missouri (MO)"),
                            ("MT", "Montana (MT)"),
                            ("NE", "Nebraska (NE)"),
                            ("NV", "Nevada (NV)"),
                            ("NH", "New Hampshire (NH)"),
                            ("NJ", "New Jersey (NJ)"),
                            ("NM", "New Mexico (NM)"),
                            ("NY", "New York (NY)"),
                            ("NC", "North Carolina (NC)"),
                            ("ND", "North Dakota (ND)"),
                            ("MP", "Northern Mariana Islands (MP)"),
                            ("OH", "Ohio (OH)"),
                            ("OK", "Oklahoma (OK)"),
                            ("OR", "Oregon (OR)"),
                            ("PA", "Pennsylvania (PA)"),
                            ("PR", "Puerto Rico (PR)"),
                            ("RI", "Rhode Island (RI)"),
                            ("SC", "South Carolina (SC)"),
                            ("SD", "South Dakota (SD)"),
                            ("TN", "Tennessee (TN)"),
                            ("TX", "Texas (TX)"),
                            ("UM", "United States Minor Outlying Islands (UM)"),
                            ("UT", "Utah (UT)"),
                            ("VT", "Vermont (VT)"),
                            ("VI", "Virgin Islands (VI)"),
                            ("VA", "Virginia (VA)"),
                            ("WA", "Washington (WA)"),
                            ("WV", "West Virginia (WV)"),
                            ("WI", "Wisconsin (WI)"),
                            ("WY", "Wyoming (WY)"),
                            ("AA", "Armed Forces Americas (AA)"),
                            ("AE", "Armed Forces Africa, Canada, Europe, Middle East (AE)"),
                            ("AP", "Armed Forces Pacific (AP)"),
                        ],
                        max_length=2,
                        null=True,
                        verbose_name="state / territory",
                    ),
                ),
                ("zipcode", models.CharField(blank=True, max_length=10, null=True, verbose_name="zip code")),
                (
                    "urbanization",
                    models.CharField(
                        blank=True, help_text="Required for Puerto Rico only", null=True, verbose_name="urbanization"
                    ),
                ),
                (
                    "security_contact_email",
                    models.EmailField(blank=True, max_length=320, null=True, verbose_name="security contact e-mail"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        help_text="Associated user",
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "federal_agency",
                    models.ForeignKey(
                        default=registrar.models.portfolio.get_default_federal_agency,
                        help_text="Associated federal agency",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="registrar.federalagency",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="domaininformation",
            name="portfolio",
            field=models.OneToOneField(
                blank=True,
                help_text="Portfolio associated with this domain",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="DomainRequest_portfolio",
                to="registrar.portfolio",
            ),
        ),
        migrations.AddField(
            model_name="domainrequest",
            name="portfolio",
            field=models.OneToOneField(
                blank=True,
                help_text="Portfolio associated with this domain",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="DomainInformation_portfolio",
                to="registrar.portfolio",
            ),
        ),
    ]
