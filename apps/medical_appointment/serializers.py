from rest_framework import serializers
from .models import MedicalAppointment


class MedicalAppointmentSerializer(serializers.ModelSerializer):
    patient_username = serializers.CharField(source="patient.username", read_only=True)

    class Meta:
        model = MedicalAppointment
        fields = [
            "id",
            "patient",
            "patient_username",
            "date",
            "time",
            "reason",
            "status",
        ]
        read_only_fields = ["id", "patient"]

    def create(self, validated_data):
        validated_data["patient"] = self.context["request"].user
        return super().create(validated_data)
