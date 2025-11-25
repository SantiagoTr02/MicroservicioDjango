
from pydantic import BaseModel
from datetime import date

class OutDTOCreatePatient(BaseModel):
    id: str
    firstName: str
    lastName: str
    birthDate: date
    gender: str
    status: str

    class Config:
        from_attributes = True
