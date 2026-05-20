# tests/routes/test_routes_acessos.py

from unittest.mock import MagicMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routes.routes_acessos import (
    roteador_usuarios,
    get_controller
)


# ==========================================
# APP TEST
# ==========================================
app = FastAPI()

app.include_router(
    roteador_usuarios
)


# ==========================================
# MOCK CONTROLLER
# ==========================================
mock_controller = MagicMock()

app.dependency_overrides[get_controller] = (
    lambda: mock_controller
)

client = TestClient(app)


# ==========================================
# CADASTRAR USUÁRIO
# ==========================================
def test_cadastrar_usuario():

    mock_controller.cadastrar_usuario.return_value = {
        "funcional": 1,
        "usuario": "jorge@gmail.com",
        "nome": "Jorge",
        "usuario_root": False,
        "usuario_ativado": True
    }

    response = client.post(
        "/usuarios/cadastro",
        json={
            "usuario": "jorge@gmail.com",
            "senha": "123456",
            "nome": "Jorge"
        }
    )

    assert response.status_code == 201

    assert response.json()["usuario"] == (
        "jorge@gmail.com"
    )

    mock_controller.cadastrar_usuario.assert_called_once()


# ==========================================
# LOGIN
# ==========================================
def test_login_usuario():

    mock_controller.login.return_value = {
        "access_token": "fake-token",
        "token_type": "bearer"
    }

    response = client.post(
        "/usuarios/login",
        json={
            "usuario": "jorge@gmail.com",
            "senha": "123456"
        }
    )

    assert response.status_code == 200

    assert response.json()["token_type"] == (
        "bearer"
    )

    mock_controller.login.assert_called_once()


# ==========================================
# LISTAR USUÁRIOS
# ==========================================
def test_listar_usuarios():

    mock_controller.listar_usuarios.return_value = [
        {
            "funcional": 1,
            "usuario": "jorge@gmail.com",
            "nome": "Jorge",
            "usuario_root": False,
            "usuario_ativado": True
        }
    ]

    response = client.get(
        "/usuarios/listar?page=1"
    )

    assert response.status_code == 200

    assert len(response.json()) == 1

    mock_controller.listar_usuarios.assert_called_once_with(
        1
    )


# ==========================================
# ALTERAR CONFIGURAÇÃO
# ==========================================
def test_alterar_configuracao_usuario():

    mock_controller.alterar_configuracao_usuario.return_value = {
        "status": "ok"
    }

    response = client.patch(
        "/usuarios/configuracao",
        json={
            "funcional": 1,
            "campo": "usuario_root"
        }
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"

    mock_controller.alterar_configuracao_usuario.assert_called_once_with(
        funcional=1,
        campo="usuario_root"
    )


# ==========================================
# ATUALIZAR USUÁRIO
# ==========================================
def test_atualizar_usuario():

    mock_controller.atualizar_usuario.return_value = {
        "status": "ok"
    }

    response = client.put(
        "/usuarios/",
        json={
            "funcional": 1,
            "nome": "Jorge Atualizado",
            "usuario": "jorge@gmail.com",
            "senha": "novaSenha123"
        }
    )

    assert response.status_code == 200

    assert response.json()["status"] == "ok"

    mock_controller.atualizar_usuario.assert_called_once()


# ==========================================
# VALIDAÇÃO CADASTRO
# ==========================================
def test_cadastrar_usuario_payload_invalido():

    response = client.post(
        "/usuarios/cadastro",
        json={
            "usuario": "email-invalido",
            "senha": "123",
            "nome": "J"
        }
    )

    assert response.status_code == 422


# ==========================================
# VALIDAÇÃO LOGIN
# ==========================================
def test_login_usuario_payload_invalido():

    response = client.post(
        "/usuarios/login",
        json={
            "usuario": "invalido",
            "senha": ""
        }
    )

    assert response.status_code == 422


# ==========================================
# VALIDAÇÃO CONFIGURAÇÃO
# ==========================================
def test_alterar_configuracao_campo_invalido():

    response = client.patch(
        "/usuarios/configuracao",
        json={
            "funcional": 1,
            "campo": "campo_invalido"
        }
    )

    assert response.status_code == 422


# ==========================================
# VALIDAÇÃO PAGE
# ==========================================
def test_listar_usuarios_page_invalida():

    response = client.get(
        "/usuarios/listar?page=0"
    )

    assert response.status_code == 422