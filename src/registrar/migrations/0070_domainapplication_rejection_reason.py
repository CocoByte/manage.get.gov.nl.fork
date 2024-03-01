# Generated by Django 4.2.7 on 2024-02-26 22:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("registrar", "0069_alter_contact_email_alter_contact_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="domainapplication",
            name="rejection_reason",
            field=models.TextField(
                blank=True,
                choices=[
                    ("purpose_not_met", "Purpose requirements not met"),
                    ("requestor_not_eligible", "Requestor not eligible to make request"),
                    ("org_has_domain", "Org already has a .gov domain"),
                    ("contacts_not_verified", "Org contacts couldn't be verified"),
                    ("org_not_eligible", "Org not eligible for a .gov domain"),
                    ("naming_not_met", "Naming requirements not met"),
                    ("other", "Other/Unspecified"),
                ],
                null=True,
            ),
        ),
    ]
