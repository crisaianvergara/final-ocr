# Generated by Django 4.1.7 on 2023-03-27 08:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("scan_receipt", "0005_scan_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scan",
            name="currency",
            field=models.CharField(max_length=4, verbose_name="Currency"),
        ),
    ]