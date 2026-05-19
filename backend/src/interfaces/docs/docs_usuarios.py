# src/interfaces/docs/docs_usuarios.py

from fastapi import status

from src.interfaces.schemas.schema_usuarios import (
    UsuarioCriacaoSchema,
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



from fastapi import status

from src.interfaces.schemas.schema_usuarios import UsuarioListagemSchema


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