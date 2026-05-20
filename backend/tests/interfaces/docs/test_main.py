# src/interfaces/docs/main.py

from fastapi.openapi.utils import get_openapi


# ==========================================
# TAGS SWAGGER
# ==========================================

tags_metadata = [

    {
        "name": "👤 Usuários",
        "description": (
            "Endpoints responsáveis por autenticação, "
            "cadastro, atualização e gerenciamento "
            "de usuários do sistema."
        )
    },

    {
        "name": "🏋️ Atividades",
        "description": (
            "Gerenciamento das atividades físicas "
            "disponíveis na plataforma."
        )
    },

    {
        "name": "📊 Atividades Praticadas",
        "description": (
            "Registro, histórico e análise "
            "das atividades realizadas pelos usuários."
        )
    }
]


# ==========================================
# CONFIGURAÇÃO OPENAPI
# ==========================================

SWAGGER_CONFIG = {

    "title": "Olympus API",

    "description": (
        "API REST desenvolvida para gerenciamento "
        "de atividades físicas, autenticação segura "
        "e análise inteligente de desempenho.\n\n"

        "## 🚀 Funcionalidades\n\n"

        "- 🔐 Autenticação JWT\n"
        "- 🛡️ Controle de acesso por perfil\n"
        "- 🏋️ Registro de atividades físicas\n"
        "- 📈 Histórico de atividades\n"
        "- 🤖 Integração com IA para análise de evolução\n"
        "- 🚨 Proteção contra brute force\n\n"

        "## 🧱 Arquitetura\n\n"

        "Projeto desenvolvido utilizando:\n\n"

        "- FastAPI\n"
        "- SQLAlchemy\n"
        "- MySQL\n"
        "- Pydantic\n"
        "- Arquitetura em camadas\n"
        "- Integração com IA Gemini\n\n"

        "## 👨‍💻 Desenvolvedor\n\n"

        "Projeto desenvolvido por Jorge Miguel "
        "como estudo avançado de backend engineering."
    ),

    "version": "2.0.0",

    "docs_url": "/docs",

    "redoc_url": "/redoc",

    "openapi_url": "/openapi.json",

    "openapi_tags": tags_metadata,

    "contact": {
        "name": "Jorge Miguel",
        "email": "jorgemiguelaviles18122001@gmail.com"
    },

    "license_info": {
        "name": "Proprietary"
    },

    "swagger_ui_parameters": {

        # mantém JWT salvo
        "persistAuthorization": True,

        # expande endpoints
        "docExpansion": "list",

        # mostra request duration
        "displayRequestDuration": True,

        # ordena tags alfabeticamente
        "tagsSorter": "alpha",

        # ordena endpoints
        "operationsSorter": "alpha",

        # dark swagger vibe
        "syntaxHighlight.theme": "monokai"
    }
}


# ==========================================
# CUSTOM OPENAPI JWT
# ==========================================

def custom_openapi(app):

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes
    )

    # ======================================
    # JWT BEARER
    # ======================================

    openapi_schema["components"]["securitySchemes"] = {

        "BearerAuth": {

            "type": "http",

            "scheme": "bearer",

            "bearerFormat": "JWT",

            "description": (
                "Insira o token JWT.\n\n"
                "Exemplo:\n"
                "`Bearer eyJhbGciOi...`"
            )
        }
    }

    # ======================================
    # PROTEÇÃO GLOBAL
    # ======================================

    openapi_schema["security"] = [
        {
            "BearerAuth": []
        }
    ]

    app.openapi_schema = openapi_schema

    return app.openapi_schema