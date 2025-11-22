from pydantic import BaseModel
from uuid import UUID

class OutDTOCreateGeneticVariant(BaseModel):
    id: str  # Convertimos el UUID a string
    geneId: int  # Devolvemos solo el ID del gene (entero)
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True  # Permite que los datos se extraigan de los objetos ORM de Django

    @classmethod
    def from_orm(cls, obj):
        # Customizamos la conversión de objetos ORM a DTO para asegurar el formato correcto
        return cls(
            id=str(obj.id),  # Convertimos el UUID a string
            geneId=obj.geneId.id,  # Extraemos solo el ID del objeto gene
            chromosome=obj.chromosome,
            position=obj.position,
            referenceBase=obj.referenceBase,
            alternateBase=obj.alternateBase,
            impact=obj.impact
        )
