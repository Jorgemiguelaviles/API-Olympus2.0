from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from src.config.database_config import Base


class ActivityModel(Base):
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
        "ActivityRequestModel",
        back_populates="atividade"
    )