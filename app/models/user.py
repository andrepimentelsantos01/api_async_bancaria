# app/models/user.py
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.account import Account

class User(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    senha_hash: str = Field(nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    contas: List["Account"] = Relationship(back_populates="usuario")
