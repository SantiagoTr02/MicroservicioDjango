from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID


class PatientInfo(BaseModel):
    id: UUID
    firstName: str
    lastName: str
    birthDate: date
    gender: str
    status: str

    class Config:
        from_attributes = True


class GeneInfo(BaseModel):
    id: int
    symbol: str
    fullName: str
    functionSummary: str

    class Config:
        from_attributes = True


class VariantInfo(BaseModel):
    id: UUID
    geneId: GeneInfo
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True


class OutDTOListPatientVariantReport(BaseModel):
    id: str
    patient: PatientInfo
    variant: VariantInfo
    detectionDate: date
    alleleFrequency: Optional[float]

    class Config:
        from_attributes = True
