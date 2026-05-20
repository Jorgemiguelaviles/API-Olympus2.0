from fastapi import (
    APIRouter,
    Depends,
    Query,
    status
)

from sqlalchemy.orm import Session

from src.config.config_banco import get_db

from src.interfaces.schemas.schema_usuarios import (
    UsuarioCriacaoSchema,
    UsuarioLoginSchema,
    UsuarioAtualizacaoSchema,
    UsuarioConfiguracaoSchema
)

from src.interfaces.docs.docs_usuarios import (
    DOC_CADASTRAR_USUARIO,
    DOC_LOGIN_USUARIO,
    DOC_ALTERAR_CONFIGURACAO,
    DOC_ATUALIZAR_USUARIO
)

from src.contollers.controller_usuarios import (
    controller_usuarios
)


roteador_usuarios = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


# ==========================================
# CADASTRO USUÁRIO
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
# LISTAR USUÁRIOS
# ==========================================
@roteador_usuarios.get(
    "/listar"
)
def listar_usuarios(
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):

    return controller_usuarios(db).listar_usuarios(page)


# ==========================================
# LOGIN
# ==========================================
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


# ==========================================
# ALTERAR CONFIGURAÇÃO
# ==========================================
@roteador_usuarios.patch(
    "/configuracao",
    **DOC_ALTERAR_CONFIGURACAO
)
def alterar_configuracao_usuario(
    payload: UsuarioConfiguracaoSchema,
    db: Session = Depends(get_db)
):

    return controller_usuarios(db).alterar_configuracao_usuario(
        funcional=payload.funcional,
        campo=payload.campo,
        valor=payload.valor
    )


# ==========================================
# ATUALIZAR USUÁRIO
# ==========================================
@roteador_usuarios.put(
    "/",
    **DOC_ATUALIZAR_USUARIO
)
def atualizar_usuario(
    payload: UsuarioAtualizacaoSchema,
    db: Session = Depends(get_db)
):

    return controller_usuarios(db).atualizar_usuario(
        funcional=payload.funcional,
        payload={
            "nome": payload.nome,
            "usuario": payload.usuario,
            "senha": payload.senha
        }
    )