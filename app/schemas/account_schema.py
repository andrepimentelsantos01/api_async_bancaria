from pydantic import BaseModel
from typing import Optional, List

class AccountBase(BaseModel):
    numero: str
    saldo: float = 0

class AccountCreate(AccountBase):
    usuario_id: int

class AccountRead(AccountBase):
    id: int

    class Config:
        from_attributes = True

class AccountWithTransactions(AccountRead):
    transacoes: List["TransactionRead"] = []

from app.schemas.account_schema import AccountRead 
from app.schemas.transaction_schema import TransactionRead
