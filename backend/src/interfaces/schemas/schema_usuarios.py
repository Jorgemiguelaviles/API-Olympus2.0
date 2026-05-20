# src/interfaces/schemas/schema_usuarios.py

from pydantic import BaseModel, EmailStr, Field,BaseModel
from typing import Optional, Literal

# ==========================================
# Cadastro
# ==========================================
class UsuarioCriacaoSchema(BaseModel):

    usuario: str = Field(..., example="jorge@gmail.com")
    senha: str = Field(..., example="Vava@0909")
    nome: str = Field(..., example="Jorge Miguel")


# ==========================================
# Resposta padrão
# ==========================================
class UsuarioRespostaSchema(BaseModel):

    funcional: int
    usuario: str
    nome: str
    usuario_root: bool
    usuario_ativado: bool

    class Config:
        from_attributes = True


# ==========================================
# Listagem paginada
# ==========================================
class UsuarioListagemSchema(BaseModel):

    funcional: int
    usuario: str
    nome: str
    usuario_root: bool
    usuario_ativado: bool

    class Config:
        from_attributes = True

class UsuarioLoginSchema(BaseModel):
    usuario: str = Field(..., example="jorge@gmail.com")
    senha: str = Field(..., example="123456")





# ==========================================
# ALTERAR ROOT
# ==========================================
class UsuarioAlterarRootSchema(BaseModel):

    funcional: int

    usuario_root: bool


# ==========================================
# ALTERAR STATUS
# ==========================================
class UsuarioAlterarStatusSchema(BaseModel):

    funcional: int

    usuario_ativado: bool


# ==========================================
# ATUALIZAR DADOS
# ==========================================
class UsuarioAtualizacaoSchema(BaseModel):

    funcional: int

    nome: Optional[str] = None

    usuario: Optional[EmailStr] = None

    senha: Optional[str] = None


class UsuarioConfiguracaoSchema(BaseModel):

    funcional: int

    campo: Literal[
        "usuario_root",
        "usuario_ativado"
    ]