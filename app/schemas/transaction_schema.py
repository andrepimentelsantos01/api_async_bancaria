from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    tipo: str = Field(..., description="Tipo da transação: 'deposito' ou 'saque'")
    valor: float = Field(..., gt=0, description="Valor positivo da transação")

class TransactionCreate(TransactionBase):
    conta_id: int

class TransactionRead(TransactionBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True
