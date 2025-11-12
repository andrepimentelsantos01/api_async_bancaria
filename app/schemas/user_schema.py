from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    nome: str
    email: EmailStr

class UserCreate(UserBase):
    senha: str

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserWithAccounts(UserRead):
    contas: List["AccountRead"] = []

from app.schemas.account_schema import AccountRead  
from app.schemas.transaction_schema import TransactionRead