from pydantic import BaseModel

class OutDTOCreateGeneticVariant(BaseModel):
    id: int
    geneId_id: int
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True
