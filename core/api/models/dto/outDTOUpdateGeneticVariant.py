from pydantic import BaseModel
from typing import Optional, Dict


class OutDTOUpdateGeneticVariant(BaseModel):
    id: str
    geneId: Dict[str, str]  # El `geneId` ahora será un diccionario con la información completa del Gene
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True
