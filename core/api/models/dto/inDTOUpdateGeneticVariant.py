from pydantic import BaseModel, Field

class InDTOUpdateGeneticVariant(BaseModel):
    chromosome: str = Field(None, example="17", description="Cromosoma donde se encuentra la variante")
    position: int = Field(None, example=412, description="Posición de la variante en el cromosoma")
    referenceBase: str = Field(None, example="A", description="Base de referencia antes de la mutación")
    alternateBase: str = Field(None, example="T", description="Base alternativa después de la mutación")
    impact: str = Field(None, example="HIGH", description="Impacto de la variante sobre el gen")

    class Config:
        str_strip_whitespace = True

