# src/interfaces/docs/docs_usuarios.py

from fastapi import status

from src.interfaces.schemas.schema_usuarios import (
    UsuarioListagemSchema,
    UsuarioRespostaSchema
)



DOC_CADASTRAR_USUARIO = {
    "response_model": UsuarioRespostaSchema,

    "summary": "Cadastrar usuário",

    "description": (
        "Cria um novo usuário no sistema."
    ),

    "responses": {
        status.HTTP_201_CREATED: {
            "description": "Usuário cadastrado com sucesso.",

            "content": {
                "application/json": {
                    "example": {
                        "funcional": 1,
                        "usuario": "jorge",
                        "nome": "Jorge Miguel",
                        "usuario_root": False,
                        "usuario_ativado": True
                    }
                }
            }
        },

        status.HTTP_400_BAD_REQUEST: {
            "description": "Dados inválidos."
        },

        status.HTTP_409_CONFLICT: {
            "description": "Usuário já existe."
        },

        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erro interno ao cadastrar usuário."
        }
    }
}




DOC_LISTAR_USUARIOS = {
    "response_model": list[UsuarioListagemSchema],

    "summary": "Listar usuários paginados",

    "description": "Retorna usuários paginados de 10 em 10 registros.",

    "responses": {
        status.HTTP_200_OK: {
            "description": "Usuários retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "funcional": 1,
                            "usuario": "jorge",
                            "nome": "Jorge Miguel",
                            "usuario_root": False,
                            "usuario_ativado": True
                        }
                    ]
                }
            }
        },

        status.HTTP_400_BAD_REQUEST: {
            "description": "Parâmetro de página inválido."
        },

        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Erro interno ao listar usuários."
        }
    }
}

DOC_LOGIN_USUARIO = {

    "summary": "Login do usuário",

    "description": (
        "Autentica usuário e retorna JWT."
    ),

    "responses": {
        200: {
            "description": "Login realizado com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJSUzI1NiIs...",
                        "token_type": "bearer"
                    }
                }
            }
        },

        401: {
            "description": "Credenciais inválidas."
        }
    }
}


# ==========================================
# ALTERAR ROOT
# ==========================================
DOC_ALTERAR_ROOT = {
    "summary": "Alterar permissão ROOT",
    "description": "Ativa ou remove permissão ROOT do usuário.",
    "responses": {
        200: {
            "description": "Permissão alterada com sucesso."
        },
        404: {
            "description": "Usuário não encontrado."
        }
    }
}


# ==========================================
# ALTERAR STATUS
# ==========================================
DOC_ALTERAR_STATUS = {
    "summary": "Ativar ou desativar usuário",
    "description": "Ativa ou desativa acesso do usuário.",
    "responses": {
        200: {
            "description": "Status alterado com sucesso."
        },
        404: {
            "description": "Usuário não encontrado."
        }
    }
}


# ==========================================
# ATUALIZAR USUÁRIO
# ==========================================
DOC_ATUALIZAR_USUARIO = {
    "summary": "Atualizar usuário",
    "description": "Atualiza nome, email e senha do usuário.",
    "responses": {
        200: {
            "description": "Usuário atualizado com sucesso."
        },
        404: {
            "description": "Usuário não encontrado."
        }
    }
}