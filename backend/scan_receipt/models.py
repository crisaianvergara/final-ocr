from django.db import models
from django.contrib.auth.models import User


class Scan(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField(max_length=30, verbose_name="Date")
    vendor = models.CharField(max_length=100, verbose_name="Vendor")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    tax = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tax")
    currency = models.CharField(max_length=3, verbose_name="Currency")
    description = models.TextField(verbose_name="Description")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User"
    )

    def __str__(self):
        return f"{self.scan_vendor} ({self.scan_amount})"
