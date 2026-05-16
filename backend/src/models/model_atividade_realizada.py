from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func

from src.config.database_config import Base


class ActivityModel(Base):
    __tablename__ = "atividade_realizada"

    id_atividade_realizada = Column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    funcional = Column(
        BigInteger,
        nullable=False
    )

    codigo_atividade = Column(
        BigInteger,
        ForeignKey("atividade.codigo_atividade"),
        nullable=False
    )

    data_hora = Column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    descricao = Column(
        String(255)
    )