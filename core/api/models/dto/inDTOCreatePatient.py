# core/api/models/dto/inDTOCreatePatient.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class InDTOCreatePatient(BaseModel):
    firstName: str
    lastName: str
    birthDate: date
    gender: str
    status: str

    class Config:
        from_attributes = True  # Permite la conversión automática
