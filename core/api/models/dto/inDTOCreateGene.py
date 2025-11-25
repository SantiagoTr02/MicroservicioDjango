from pydantic import BaseModel

class InDTOCreateGene(BaseModel):
    symbol: str
    fullName: str
    functionSummary: str
    class Config:
        str_strip_whitespace = True
