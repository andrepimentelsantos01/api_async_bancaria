from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.account import Account

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    email: str = Field(index=True, unique=True)
    senha_hash: str
    criado_em: datetime = Field(default_factory=datetime.utcnow)

    contas: List["Account"] = Relationship(back_populates="usuario")
