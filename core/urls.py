from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.login.urls")),
    path("api/", include("apps.medical_appointment.urls")),
]
