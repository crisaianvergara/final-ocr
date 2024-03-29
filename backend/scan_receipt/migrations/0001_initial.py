# Generated by Django 4.1.7 on 2023-03-26 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Scan",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("date", models.CharField(max_length=30, verbose_name="Date")),
                ("vendor", models.CharField(max_length=100, verbose_name="Vendor")),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Amount"
                    ),
                ),
                (
                    "tax",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Tax"
                    ),
                ),
                ("currency", models.CharField(max_length=3, verbose_name="Currency")),
                ("description", models.TextField(verbose_name="Description")),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
        ),
    ]
