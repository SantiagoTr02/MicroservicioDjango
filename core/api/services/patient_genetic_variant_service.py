# core/api/services/patient_genetic_variant_service.py
from uuid import uuid4
import requests

from django.conf import settings

from ..exceptions.patient_genetic_variant_exceptions import PatientGeneticVariantAlreadyExistsException, \
    PatientGeneticVariantFieldNotFilledException, PatientGeneticVariantInvalidDataFormatException
from ..models.entities.patient_genetic_variant import PatientGeneticVariant
from ..models.entities.patient import Patient
from ..models.entities.genetic_variant import GeneticVariant

class GeneticVariantPatientService:
    @staticmethod
    def assign_variant_to_patient(patientId, variantId, detectionDate, alleleFrequency):
        # Validar campos obligatorios antes de pasar a Pydantic
        if not patientId:
            raise PatientGeneticVariantFieldNotFilledException("The field 'patientId' is required.")
        if not variantId:
            raise PatientGeneticVariantFieldNotFilledException("The field 'variantId' is required.")
        if not detectionDate:
            raise PatientGeneticVariantFieldNotFilledException("The field 'detectionDate' is required.")
        if alleleFrequency is None:
            raise PatientGeneticVariantFieldNotFilledException("The field 'alleleFrequency' is required.")

        # Validar existencia del paciente
        try:
            patient = Patient.objects.get(id=patientId)
        except Patient.DoesNotExist:
            # Intentar consultar el microservicio externo de pacientes
            try:
                external_base = getattr(settings, 'EXTERNAL_PATIENT_SERVICE_BASE', 'http://clinic:3000')
                url = f"{external_base.rstrip('/')}/patients/{patientId}"
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    # Crear paciente localmente con los campos mínimos que tengamos
                    patient = Patient.objects.create(
                        id=data.get('id'),
                        firstName=data.get('firstName', '')[:100],
                        lastName=data.get('lastName', '')[:100],
                        birthDate=data.get('birthDate') or '1900-01-01',
                        gender=data.get('gender', 'Other'),
                        status=data.get('status', 'Activo'),
                    )
                else:
                    return {"detail": "Patient not found"}, 404
            except requests.RequestException:
                return {"detail": "Patient not found"}, 404

        # Validar existencia de la variante genética
        try:
            variant = GeneticVariant.objects.get(id=variantId)
        except GeneticVariant.DoesNotExist:
            return {"detail": "Genetic variant not found"}, 404

        # Crear la relación (OJO: usar patient_id / variant_id)
        relation = PatientGeneticVariant.objects.create(
            patient_id=patientId,       # <- nombre del campo: patient
            variant_id=variantId,       # <- nombre del campo: variant
            detectionDate=detectionDate,
            alleleFrequency=alleleFrequency
        )

        return relation

    @staticmethod
    def list_patient_variant_reports():
        return PatientGeneticVariant.objects.select_related(
            "patient",          # FK a Patient
            "variant__geneId"   # FK de Variant a Gene
        ).all()
