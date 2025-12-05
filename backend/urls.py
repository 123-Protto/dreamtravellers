from django.contrib import admin
from django.urls import path, include
from .views import home   # <-- YOU FORGOT THIS

urlpatterns = [
    path("", home),  # Homepage route
    path("admin/", admin.site.urls),
    path("api/", include("enquiries.urls")),
]
