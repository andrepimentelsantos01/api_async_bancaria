from __future__ import annotations
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.transaction import Transaction

class Account(SQLModel, table=True):
    __tablename__ = "contas"

    id: Optional[int] = Field(default=None, primary_key=True)
    numero: str = Field(index=True, unique=True, nullable=False)
    saldo: float = Field(default=0, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    usuario_id: int = Field(foreign_key="usuarios.id", nullable=False)
    usuario: "User" = Relationship(back_populates="contas")
    transacoes: List["Transaction"] = Relationship(back_populates="conta")
