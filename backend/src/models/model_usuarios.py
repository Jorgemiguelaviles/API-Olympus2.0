# src/models/model_usuarios.py

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean
)

from sqlalchemy.orm import relationship

from src.config.config_banco import Base


class model_usuarios(Base):
    __tablename__ = "usuarios"

    funcional = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    usuario = Column(
        String(50),
        nullable=False,
        unique=True
    )

    senha_hash = Column(
        String(255),
        nullable=False
    )

    nome = Column(
        String(100),
        nullable=False
    )

    usuario_root = Column(
        Boolean,
        nullable=False,
        default=False
    )

    usuario_ativado = Column(
        Boolean,
        nullable=False,
        default=True
    )

    atividades_realizadas = relationship(
        "model_atividades_realizadas",
        back_populates="usuario"
    )
