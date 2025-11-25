from pydantic import BaseModel
from typing import Optional

class InDTOUpdateGeneticVariant(BaseModel):
    geneId: Optional[int]
    chromosome: Optional[str]
    position: Optional[int]
    referenceBase: Optional[str]
    alternateBase: Optional[str]
    impact: Optional[str]

    class Config:
        from_attributes = True
