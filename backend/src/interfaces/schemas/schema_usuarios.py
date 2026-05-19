# src/interfaces/schema_usuarios.py

from pydantic import BaseModel, Field


class UsuarioCriacaoSchema(BaseModel):

    usuario: str = Field(
        ...,
        example="jorge"
    )

    senha: str = Field(
        ...,
        example="123456"
    )

    nome: str = Field(
        ...,
        example="Jorge Miguel"
    )


class UsuarioRespostaSchema(BaseModel):

    funcional: int
    usuario: str
    nome: str
    usuario_root: bool
    usuario_ativado: bool

    class Config:
        from_attributes = True