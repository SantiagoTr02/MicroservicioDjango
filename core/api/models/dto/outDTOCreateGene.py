from pydantic import BaseModel

class OutDTOCreateGene(BaseModel):
    id: int
    symbol: str
    fullName: str
    functionSummary: str

    class Config:
        from_attributes = True  # Habilita la compatibilidad con ORM (Django Models)
