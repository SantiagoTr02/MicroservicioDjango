# core/api/models/dto/outDTOAssignVariantToPatient.py
from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class OutDTOAssignVariantToPatient(BaseModel):
    id: UUID
    patientId: UUID
    variantId: UUID
    detectionDate: date
    alleleFrequency: Optional[float]

    class Config:
        from_attributes = True
