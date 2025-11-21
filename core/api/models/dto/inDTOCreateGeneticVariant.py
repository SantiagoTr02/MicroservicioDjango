from pydantic import BaseModel, Field

class InDTOCreateGeneticVariant(BaseModel):
    geneId_id: int = Field(..., example=1, description="ID del gen asociado a la variante")
    chromosome: str = Field(..., example="17", description="Cromosoma donde se encuentra la variante")
    position: int = Field(..., example=412, description="Posición de la variante en el cromosoma")
    referenceBase: str = Field(..., example="A", description="Base de referencia antes de la mutación")
    alternateBase: str = Field(..., example="T", description="Base alternativa después de la mutación")
    impact: str = Field(..., example="HIGH", description="Impacto de la variante sobre el gen")

    class Config:
        str_strip_whitespace = True

