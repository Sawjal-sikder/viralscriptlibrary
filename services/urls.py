from django.urls import path
from .views import *

urlpatterns = [
    path("packages/", PackageView.as_view(), name="package-list-create"),
    path("packages/<int:pk>/", PackageRetrieveUpdateDestroyAPIView.as_view(), name="package-detail"),
]
