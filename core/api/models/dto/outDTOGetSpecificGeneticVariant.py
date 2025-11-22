from pydantic import BaseModel
from typing import Dict

class OutDTOGetSpecificGeneticVariant(BaseModel):
    id: str
    geneId: Dict[str, str]  # El geneId será un diccionario con el ID y otros detalles del gene
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True  # Esto permite convertir el objeto ORM a un modelo Pydantic
