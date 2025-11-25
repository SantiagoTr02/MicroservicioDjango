from pydantic import BaseModel
from uuid import UUID

class OutDTOCreateGeneticVariant(BaseModel):
    id: str
    geneId: int
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=str(obj.id),
            geneId=obj.geneId.id,
            chromosome=obj.chromosome,
            position=obj.position,
            referenceBase=obj.referenceBase,
            alternateBase=obj.alternateBase,
            impact=obj.impact
        )
