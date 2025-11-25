from pydantic import BaseModel

class OutDTOListGene(BaseModel):
    id: int
    symbol: str
    fullName: str
    functionSummary: str

    class Config:
        from_attributes = True
