from django.contrib import admin
from django.urls import path, include
from scan_receipt import urls as scan_receipt_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("scans/", include(scan_receipt_urls)),
]
