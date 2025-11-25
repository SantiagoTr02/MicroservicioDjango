# core/api/views/patient_genetic_variant_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pydantic import ValidationError

from ..exceptions.patient_genetic_variant_exceptions import PatientGeneticVariantAlreadyExistsException, \
    PatientGeneticVariantInvalidDataFormatException, PatientGeneticVariantFieldNotFilledException
from ..services.patient_genetic_variant_service import GeneticVariantPatientService
from ..models.dto.inDTOAssignVariantToPatient import InDTOAssignVariantToPatient
from ..models.dto.outDTOAssignVariantToPatient import OutDTOAssignVariantToPatient
from ..models.dto.outDTOListPatientVariantReport import OutDTOListPatientVariantReport


class AssignGeneticVariantToPatientView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            assign_data = InDTOAssignVariantToPatient(**request.data)

            result = GeneticVariantPatientService.assign_variant_to_patient(
                assign_data.patientId,
                assign_data.variantId,
                assign_data.detectionDate,
                assign_data.alleleFrequency
            )

            if isinstance(result, tuple):
                return Response(result[0], status=result[1])

            response_data = OutDTOAssignVariantToPatient(
                id=result.id,
                patientId=str(result.patient.id),
                variantId=str(result.variant.id),
                detectionDate=result.detectionDate,
                alleleFrequency=float(result.alleleFrequency) if result.alleleFrequency is not None else None
            )

            return Response(response_data.dict(), status=status.HTTP_201_CREATED)

        except PatientGeneticVariantAlreadyExistsException as e:
            return Response(
                {"error": "VARIANT_ALREADY_ASSIGNED", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PatientGeneticVariantFieldNotFilledException as e:
            return Response(
                {"error": "FIELD_NOT_FILLED", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except PatientGeneticVariantInvalidDataFormatException as e:
            return Response(
                {"error": "INVALID_DATA_FORMAT", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            # Errores de Pydantic (tipos, campos faltantes, etc.)
            return Response(
                {"error": "VALIDATION_ERROR", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ListPatientVariantReportsView(APIView):
    def get(self, request, *args, **kwargs):
        relations = GeneticVariantPatientService.list_patient_variant_reports()

        response = []

        for rel in relations:
            patient = rel.patient          # <- aquí
            variant = rel.variant          # <- aquí
            gene = variant.geneId

            dto = OutDTOListPatientVariantReport(
                id=rel.id,
                patient={
                    "id": patient.id,
                    "firstName": patient.firstName,
                    "lastName": patient.lastName,
                    "birthDate": patient.birthDate,
                    "gender": patient.gender,
                    "status": patient.status,
                },
                variant={
                    "id": variant.id,
                    "geneId": {
                        "id": gene.id,
                        "symbol": gene.symbol,
                        "fullName": gene.fullName,
                        "functionSummary": gene.functionSummary,
                    },
                    "chromosome": variant.chromosome,
                    "position": variant.position,
                    "referenceBase": variant.referenceBase,
                    "alternateBase": variant.alternateBase,
                    "impact": variant.impact,
                },
                detectionDate=rel.detectionDate,
                alleleFrequency=float(rel.alleleFrequency) if rel.alleleFrequency is not None else None,
            )

            response.append(dto.dict())

        return Response(response, status=status.HTTP_200_OK)
