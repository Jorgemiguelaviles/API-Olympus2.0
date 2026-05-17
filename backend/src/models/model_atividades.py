from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.config.config_banco import Base


class model_atividades(Base):
    __tablename__ = "atividade"

    codigo_atividade = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    nome_atividade = Column(
        String(50),
        nullable=False,
        unique=True
    )

    atividades_realizadas = relationship(
        "model_atividades_realizadas",
        back_populates="atividade"
    )