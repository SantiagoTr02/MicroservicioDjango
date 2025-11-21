from pydantic import BaseModel, Field

class InDTOUpdateGene(BaseModel):
    symbol: str = Field(None, example="BRCA1", description="Símbolo único del gen")
    fullName: str = Field(None, example="Breast Cancer 1", description="Nombre completo del gen")
    functionSummary: str = Field(None, example="Gene associated with breast cancer risk", description="Descripción funcional del gen")

    class Config:
        str_min_length = 1
        str_strip_whitespace = True
