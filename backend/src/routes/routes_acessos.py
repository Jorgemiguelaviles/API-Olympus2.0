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
    DOC_LISTAR_USUARIOS,
    DOC_ALTERAR_CONFIGURACAO,
    DOC_ATUALIZAR_USUARIO
)

from src.contollers.controller_usuarios import (
    controller_usuarios
)


# ==========================================
# ROUTER
# ==========================================
roteador_usuarios = APIRouter(
    prefix="/usuarios",
    tags=["👤 Usuários"]
)


# ==========================================
# DEPENDENCY
# ==========================================
def get_controller(
    db: Session = Depends(get_db)
):
    return controller_usuarios(db)


# ==========================================
# CADASTRAR
# ==========================================
@roteador_usuarios.post(
    "/cadastro",
    status_code=status.HTTP_201_CREATED,
    **DOC_CADASTRAR_USUARIO
)
def cadastrar_usuario(
    payload: UsuarioCriacaoSchema,
    controller = Depends(get_controller)
):

    return controller.cadastrar_usuario(
        payload.model_dump()
    )


# ==========================================
# LOGIN
# ==========================================
@roteador_usuarios.post(
    "/login",
    **DOC_LOGIN_USUARIO
)
def login_usuario(
    payload: UsuarioLoginSchema,
    controller = Depends(get_controller)
):

    return controller.login(
        payload.model_dump()
    )


# ==========================================
# LISTAR
# ==========================================
@roteador_usuarios.get(
    "/listar",
    **DOC_LISTAR_USUARIOS
)
def listar_usuarios(
    page: int = Query(
        1,
        ge=1,
        description="Número da página"
    ),
    controller = Depends(get_controller)
):

    return controller.listar_usuarios(page)


# ==========================================
# CONFIGURAÇÃO
# ==========================================
@roteador_usuarios.patch(
    "/configuracao",
    **DOC_ALTERAR_CONFIGURACAO
)
def alterar_configuracao_usuario(
    payload: UsuarioConfiguracaoSchema,
    controller = Depends(get_controller)
):

    return controller.alterar_configuracao_usuario(
        funcional=payload.funcional,
        campo=payload.campo
    )


# ==========================================
# ATUALIZAR
# ==========================================
@roteador_usuarios.put(
    "/",
    **DOC_ATUALIZAR_USUARIO
)
def atualizar_usuario(
    payload: UsuarioAtualizacaoSchema,
    controller = Depends(get_controller)
):

    return controller.atualizar_usuario(
        funcional=payload.funcional,
        payload=payload.model_dump()
    )