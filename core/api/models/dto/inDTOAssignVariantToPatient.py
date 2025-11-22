# core/api/models/dto/inDTOAssignVariantToPatient.py
from pydantic import BaseModel
from uuid import UUID
from datetime import date

class InDTOAssignVariantToPatient(BaseModel):
    patientId: UUID  # ID del paciente
    variantId: UUID  # ID de la variante genética
    detectionDate: date  # Fecha de detección de la variante
    alleleFrequency: float  # Frecuencia alélica

    class Config:
        from_attributes = True  # Permite la conversión automática
