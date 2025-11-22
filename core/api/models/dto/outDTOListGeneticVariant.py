from pydantic import BaseModel
from typing import Dict

class OutDTOListGeneticVariant(BaseModel):
    id: str
    geneId: Dict[str, str]  # Aquí seguimos con el formato de diccionario para la información del gene
    chromosome: str
    position: int
    referenceBase: str
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True  # Permite que los datos se extraigan de los objetos ORM de Django

    @classmethod
    def from_orm(cls, obj):
        """Este metodo personaliza la conversión del objeto ORM a DTO."""
        return cls(
            id=str(obj.id),  # Convertimos el UUID a string
            geneId={
                "id": str(obj.geneId.id),  # Aquí convertimos el id a string para cumplir con el tipo de pydantic
                "symbol": obj.geneId.symbol,
                "fullName": obj.geneId.fullName,
                "functionSummary": obj.geneId.functionSummary
            },
            chromosome=obj.chromosome,
            position=obj.position,
            referenceBase=obj.referenceBase,
            alternateBase=obj.alternateBase,
            impact=obj.impact
        )
