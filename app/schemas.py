from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class DespesaBase(BaseModel):
    descricao: str
    valor: float
    categoria: str


class DespesaCreate(DespesaBase):
    pass


class DespesaResponse(DespesaBase):
    id: int
    data: datetime

    class Config:
        from_attributes = True