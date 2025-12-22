from django.urls import path
from .views import (
    ListAppointmentsView,
    CreateAppointmentView,
    UpdateAppointmentView,
    DeleteAppointmentView,
    ChatView,
)

urlpatterns = [
    path(
        "appointments/list/", ListAppointmentsView.as_view(), name="list-appointments"
    ),
    path(
        "appointments/create/",
        CreateAppointmentView.as_view(),
        name="create-appointment",
    ),
    path(
        "appointments/<int:appointment_id>/update/",
        UpdateAppointmentView.as_view(),
        name="update-appointment",
    ),
    path(
        "appointments/<int:appointment_id>/delete/",
        DeleteAppointmentView.as_view(),
        name="delete-appointment",
    ),
    path("chat/", ChatView.as_view(), name="chat"),
]
