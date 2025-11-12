# app/models/account.py
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction

class Account(SQLModel, table=True):
    __tablename__ = "contas"

    id: Optional[int] = Field(default=None, primary_key=True)
    numero: str = Field(index=True, unique=True, nullable=False)
    saldo: float = Field(default=0.0, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    usuario: "User" = Relationship(back_populates="contas")

    transacoes: List["Transaction"] = Relationship(back_populates="conta")
