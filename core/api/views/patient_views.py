# core/api/views/patient_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.patient_service import PatientService
from ..models.dto.inDTOCreatePatient import InDTOCreatePatient
from ..models.dto.outDTOCreatePatient import OutDTOCreatePatient
from pydantic import ValidationError

class CreatePatientView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            #Valida los datos de entrada usando InDTOCreatePatient
            patient_data = InDTOCreatePatient(**request.data)

            #Usa el servicio para crear el paciente
            result = PatientService.create_patient(patient_data.dict())

            #El servicio devuelve una Response
            return Response(result.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
