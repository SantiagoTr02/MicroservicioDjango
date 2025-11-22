from pydantic import BaseModel

class InDTOCreateGeneticVariant(BaseModel):
    geneId: int
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str
