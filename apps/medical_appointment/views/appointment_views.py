from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import MedicalAppointment
from ..serializers import MedicalAppointmentSerializer


class ListAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Lista todas las citas del usuario autenticado"""
        appointments = MedicalAppointment.objects.filter(patient=request.user)
        serializer = MedicalAppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Crea una nueva cita médica"""
        serializer = MedicalAppointmentSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, appointment_id):
        """Actualiza una cita médica existente (PUT)"""
        return self._update(request, appointment_id, partial=False)

    def patch(self, request, appointment_id):
        """Actualiza una cita médica existente (PATCH)"""
        return self._update(request, appointment_id, partial=True)

    def _update(self, request, appointment_id, partial=False):
        try:
            appointment = MedicalAppointment.objects.get(
                id=appointment_id, patient=request.user
            )
        except MedicalAppointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = MedicalAppointmentSerializer(
            appointment,
            data=request.data,
            partial=partial,
            context={"request": request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, appointment_id):
        """Elimina una cita médica"""
        try:
            appointment = MedicalAppointment.objects.get(
                id=appointment_id, patient=request.user
            )
        except MedicalAppointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
