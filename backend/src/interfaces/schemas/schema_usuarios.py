from typing import Optional, Literal

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict
)


# ==========================================
# CADASTRO
# ==========================================
class UsuarioCriacaoSchema(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "usuario": "jorge@gmail.com",
                "senha": "Vava@0909",
                "nome": "Jorge Miguel"
            }
        }
    )

    usuario: EmailStr = Field(
        ...,
        description="Email do usuário"
    )

    senha: str = Field(
        ...,
        min_length=6,
        description="Senha de autenticação"
    )

    nome: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome completo do usuário"
    )


# ==========================================
# LOGIN
# ==========================================
class UsuarioLoginSchema(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "usuario": "jorge@gmail.com",
                "senha": "123456"
            }
        }
    )

    usuario: EmailStr = Field(
        ...,
        description="Email do usuário"
    )

    senha: str = Field(
        ...,
        description="Senha do usuário"
    )


# ==========================================
# RESPONSE PADRÃO
# ==========================================
class UsuarioRespostaSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    funcional: int = Field(
        description="Identificador funcional"
    )

    usuario: str = Field(
        description="Email/login do usuário"
    )

    nome: str = Field(
        description="Nome completo"
    )

    usuario_root: bool = Field(
        description="Define se o usuário possui acesso ROOT"
    )

    usuario_ativado: bool = Field(
        description="Define se o usuário está ativo"
    )


# ==========================================
# LISTAGEM
# ==========================================
class UsuarioListagemSchema(UsuarioRespostaSchema):
    pass


# ==========================================
# ALTERAR CONFIGURAÇÃO
# ==========================================
class UsuarioConfiguracaoSchema(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "funcional": 100000000,
                "campo": "usuario_root"
            }
        }
    )

    funcional: int = Field(
        description="Funcional do usuário"
    )

    campo: Literal[
        "usuario_root",
        "usuario_ativado"
    ] = Field(
        description="Campo que será alterado"
    )


# ==========================================
# ATUALIZAR USUÁRIO
# ==========================================
class UsuarioAtualizacaoSchema(BaseModel):

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "funcional": 100000000,
                "nome": "Jorge Miguel",
                "usuario": "jorge@gmail.com",
                "senha": "novaSenha123"
            }
        }
    )

    funcional: int

    nome: Optional[str] = None

    usuario: Optional[EmailStr] = None

    senha: Optional[str] = None