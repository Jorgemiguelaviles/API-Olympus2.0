# ==========================================
# TAGS SWAGGER
# ==========================================



# ==========================================
# CONFIGURAÇÃO OPENAPI
# ==========================================

SWAGGER_CONFIG = {

    "title": "Olympus API",

    "description": (
        "API REST desenvolvida para gerenciamento "
        "de atividades físicas, autenticação segura "
        "e análise inteligente de desempenho.\n\n"

        "## Funcionalidades\n"

        "- Autenticação JWT\n"
        "- Controle de acesso por perfil\n"
        "- Registro de atividades físicas\n"
        "- Histórico de atividades\n"
        "- Integração com IA para análise de evolução\n"
        "- Proteção contra brute force\n\n"

        "Projeto desenvolvido utilizando "
        "FastAPI, SQLAlchemy e arquitetura em camadas."
    ),

    "version": "2.0.0",

    "docs_url": "/docs",

    "redoc_url": "/redoc",

    "openapi_url": "/openapi.json",

    "contact": {
        "name": "Jorge Miguel",
        "email": "jorgemiguelaviles18122001@gmail.com"
    },

    "license_info": {
        "name": "Proprietary"
    },

    "swagger_ui_parameters": {
        "persistAuthorization": True
    }
}