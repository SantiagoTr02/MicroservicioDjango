from rest_framework.response import Response
from rest_framework import status
from ..models.entities.patient import Patient
from ..models.dto.outDTOCreatePatient import OutDTOCreatePatient

class PatientService:
    @staticmethod
    def create_patient(data: dict):
        # Crear el paciente en la base de datos
        patient = Patient.objects.create(**data)

        # Convertir el ID de UUID a string antes de pasarlo al DTO
        response_data = OutDTOCreatePatient(
            id=str(patient.id),  # Convertir el UUID a string
            firstName=patient.firstName,
            lastName=patient.lastName,
            birthDate=patient.birthDate,
            gender=patient.gender,
            status=patient.status
        )

        # Devolver la respuesta con el DTO convertido a diccionario
        return Response(response_data.dict(), status=status.HTTP_201_CREATED)
