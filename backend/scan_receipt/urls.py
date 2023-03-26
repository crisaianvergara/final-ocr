from django.urls import path
from .views import ScanListAPIView, ScanDetailApiView


urlpatterns = [
    path("api/", ScanListAPIView.as_view()),
    path("api/<int:scan_id>/", ScanDetailApiView.as_view()),
]
