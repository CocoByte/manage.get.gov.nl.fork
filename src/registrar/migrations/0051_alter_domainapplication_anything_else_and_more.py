# Generated by Django 4.2.7 on 2023-11-29 16:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("registrar", "0050_alter_domainapplication_anything_else_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="domainapplication",
            name="anything_else",
            field=models.TextField(blank=True, help_text="Anything else we should know?", null=True),
        ),
        migrations.AlterField(
            model_name="domaininformation",
            name="anything_else",
            field=models.TextField(blank=True, help_text="Anything else we should know?", null=True),
        ),
    ]
