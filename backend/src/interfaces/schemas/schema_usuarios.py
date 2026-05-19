# src/interfaces/schemas/schema_usuarios.py

from pydantic import BaseModel, Field


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