from fastapi import (
    APIRouter,
    Depends,
    Query,
    status,
    HTTPException
)

from sqlalchemy.orm import Session

from src.config.config_banco import get_db

from src.interfaces.schemas.schema_usuarios import (
    UsuarioCriacaoSchema,
    UsuarioLoginSchema
)

from src.interfaces.docs.docs_usuarios import (
    DOC_CADASTRAR_USUARIO,
    DOC_LOGIN_USUARIO
)

from src.contollers.controller_usuarios import (
    controller_usuarios
)

from src.services.service_seguranca.jwt import create_access_token



roteador_usuarios = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


# ==========================================
# Cadastro de usuário
# ==========================================
@roteador_usuarios.post(
    "/cadastro",
    status_code=status.HTTP_201_CREATED,
    **DOC_CADASTRAR_USUARIO
)
def cadastrar_usuario(
    payload: UsuarioCriacaoSchema,
    db: Session = Depends(get_db)
):

    return controller_usuarios(db).cadastrar_usuario({
        "usuario": payload.usuario,
        "senha": payload.senha,
        "nome": payload.nome
    })


# ==========================================
# Listar usuários
# ==========================================
@roteador_usuarios.get("/listar")
def listar_usuarios(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):

    return controller_usuarios(db).listar_usuarios(page)

@roteador_usuarios.post(
    "/login",
    **DOC_LOGIN_USUARIO
)
def login_usuario(
    payload: UsuarioLoginSchema,
    db: Session = Depends(get_db)
):

    return controller_usuarios(db).login({
        "usuario": payload.usuario,
        "senha": payload.senha
    })