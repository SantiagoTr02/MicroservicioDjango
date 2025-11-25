from pydantic import BaseModel
from typing import Dict

class OutDTOGetSpecificGeneticVariant(BaseModel):
    id: str
    geneId: Dict[str, str]
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True
