from pydantic import BaseModel
from typing import Optional

class InDTOUpdateGeneticVariant(BaseModel):
    geneId: Optional[int]  # Ahora es un diccionario que representará el objeto completo del Gene
    chromosome: Optional[str]
    position: Optional[int]
    referenceBase: Optional[str]
    alternateBase: Optional[str]
    impact: Optional[str]

    class Config:
        from_attributes = True
