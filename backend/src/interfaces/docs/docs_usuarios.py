from fastapi import status

from src.interfaces.schemas.schema_usuarios import (
    UsuarioRespostaSchema,
    UsuarioListagemSchema
)


# ==========================================
# CADASTRAR USUÁRIO
# ==========================================
DOC_CADASTRAR_USUARIO = {

    "response_model": UsuarioRespostaSchema,

    "summary": "Cadastrar usuário",

    "description": (
        "Cria um novo usuário no sistema."
    ),

    "responses": {

        status.HTTP_201_CREATED: {
            "description": "Usuário cadastrado com sucesso."
        },

        status.HTTP_400_BAD_REQUEST: {
            "description": "Dados inválidos."
        },

        status.HTTP_409_CONFLICT: {
            "description": "Usuário já existente."
        }
    }
}


# ==========================================
# LOGIN
# ==========================================
DOC_LOGIN_USUARIO = {

    "summary": "Autenticar usuário",

    "description": (
        "Realiza autenticação e retorna JWT."
    ),

    "responses": {

        status.HTTP_200_OK: {
            "description": "Login realizado com sucesso."
        },

        status.HTTP_401_UNAUTHORIZED: {
            "description": "Credenciais inválidas."
        }
    }
}


# ==========================================
# LISTAR USUÁRIOS
# ==========================================
DOC_LISTAR_USUARIOS = {

    "response_model": list[UsuarioListagemSchema],

    "summary": "Listar usuários",

    "description": (
        "Retorna usuários paginados."
    )
}


# ==========================================
# ALTERAR CONFIGURAÇÃO
# ==========================================
DOC_ALTERAR_CONFIGURACAO = {

    "summary": "Alterar configuração do usuário",

    "description": (
        "Altera permissões e status do usuário."
    )
}


# ==========================================
# ATUALIZAR USUÁRIO
# ==========================================
DOC_ATUALIZAR_USUARIO = {

    "summary": "Atualizar usuário",

    "description": (
        "Atualiza dados do usuário."
    )
}