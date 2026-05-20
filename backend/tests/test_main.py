# tests/test_main.py

from fastapi import FastAPI
from fastapi.routing import APIRoute

from src.main import app

from src.middlewares.bearer import (
    AuthMiddleware
)


# ==========================================
# APP EXISTE
# ==========================================
def test_app_instance():

    assert isinstance(
        app,
        FastAPI
    )


# ==========================================
# TITLE
# ==========================================
def test_app_title():

    assert app.title == "Olympus API"


# ==========================================
# VERSION
# ==========================================
def test_app_version():

    assert app.version == "2.0.0"


# ==========================================
# DOCS URL
# ==========================================
def test_docs_url():

    assert app.docs_url == "/docs"


# ==========================================
# REDOC URL
# ==========================================
def test_redoc_url():

    assert app.redoc_url == "/redoc"


# ==========================================
# OPENAPI URL
# ==========================================
def test_openapi_url():

    assert app.openapi_url == "/openapi.json"


# ==========================================
# MIDDLEWARE REGISTRADO
# ==========================================
def test_auth_middleware_exists():

    middlewares = [
        middleware.cls
        for middleware in app.user_middleware
    ]

    assert AuthMiddleware in middlewares


# ==========================================
# ROTAS USUÁRIOS
# ==========================================
def test_rotas_usuarios_registradas():

    paths = [
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    ]

    assert "/usuarios/login" in paths

    assert "/usuarios/cadastro" in paths

    assert "/usuarios/listar" in paths


# ==========================================
# ROTAS ATIVIDADES
# ==========================================
def test_rotas_atividades_registradas():

    paths = [
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    ]

    assert "/atividades/opcoes" in paths


# ==========================================
# ROTAS ATIVIDADES PRATICADAS
# ==========================================
def test_rotas_atividades_praticadas_registradas():

    paths = [
        route.path
        for route in app.routes
        if isinstance(route, APIRoute)
    ]

    assert "/atividadespraticadas/" in paths

    assert "/atividadespraticadas/minhas" in paths


# ==========================================
# OPENAPI GERADA
# ==========================================
def test_openapi_schema():

    schema = app.openapi()

    assert schema["info"]["title"] == (
        "Olympus API"
    )

    assert schema["info"]["version"] == (
        "2.0.0"
    )


# ==========================================
# TAGS EXISTEM
# ==========================================
def test_tags_existentes():

    schema = app.openapi()

    tags = schema.get("tags", [])

    assert isinstance(tags, list)