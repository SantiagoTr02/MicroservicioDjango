from pydantic import BaseModel

class OutDTOListGeneticVariant(BaseModel):
    id: int
    geneId_id: int  # Asegúrate de que el nombre coincida con la columna en la base de datos
    chromosome: str
    position: int
    referenceBase: str  # Usamos camelCase para los nombres en Pydantic
    alternateBase: str
    impact: str

    class Config:
        from_attributes = True  # Para permitir la conversión de objetos ORM a Pydantic model
