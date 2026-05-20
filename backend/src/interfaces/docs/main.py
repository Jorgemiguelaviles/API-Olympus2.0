# src/docs/swagger_config.py

# ==========================================

# TAGS SWAGGER

# ==========================================

tags_metadata = [
{
"name": "Usuários",
"description": (
"Operações relacionadas a cadastro, "
"autenticação e gerenciamento de usuários."
)
},
{
"name": "Atividades",
"description": (
"Gestão das atividades físicas "
"disponíveis no sistema."
)
},
{
"name": "Atividades Praticadas",
"description": (
"Registro e consulta das atividades "
"realizadas pelos usuários."
)
}
]

# ==========================================

# CONFIGURAÇÃO OPENAPI

# ==========================================

SWAGGER_CONFIG = {

"title": "Olympus API",

"description": (
    "API para gerenciamento de atividades físicas "
    "e controle de usuários.\n\n"

    "Sistema com autenticação JWT, "
    "controle de acesso por usuário root "
    "e proteção contra brute force."
),

"version": "1.0.0",

"openapi_tags": tags_metadata,

"contact": {
    "name": "Olympus Support",
    "email": "suporte@olympus.api"
},

"license_info": {
    "name": "Proprietary"
}

}
