from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AtividadeCriacaoSchema(BaseModel):
    funcional: int = Field(
        ...,
        example=12345,
        description="Identificador funcional do usuário"
    )

    codigo_atividade: str = Field(
        ...,
        example='RUN',
        description="Código da atividade física"
    )

    descricao: Optional[str] = Field(
        None,
        example="Corrida de 5km no parque",
        description="Descrição opcional da atividade realizada"
    )


class AtividadeRespostaSchema(BaseModel):
    funcional: int
    codigo_atividade: str
    descricao: Optional[str]
    data_hora: datetime

    class Config:
        from_attributes = True

class AtividadeExistenteResponseSchema(BaseModel):
    codigo_atividade: str

    class Config:
        from_attributes = True