# core/api/models/dto/outDTOCreatePatient.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class OutDTOCreatePatient(BaseModel):
    id: str
    firstName: str
    lastName: str
    birthDate: date
    gender: str
    status: str

    class Config:
        from_attributes = True  # Permite la conversión automática
