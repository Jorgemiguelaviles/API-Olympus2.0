from unittest.mock import MagicMock
from types import SimpleNamespace

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

app.include_router(roteador_usuarios)


# 🔥 FIX ESSENCIAL: mock do request.state.user
@app.middleware("http")
async def add_user_to_state(request, call_next):
    request.state.user = SimpleNamespace(id=1)
    return await call_next(request)


# ==========================================
# MOCK CONTROLLER
# ==========================================
mock_controller = MagicMock()

app.dependency_overrides[get_controller] = lambda: mock_controller

client = TestClient(app)



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
    assert response.json()["usuario"] == "jorge@gmail.com"

    mock_controller.cadastrar_usuario.assert_called_once()



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
    assert response.json()["token_type"] == "bearer"

    mock_controller.login.assert_called_once()


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

    response = client.get("/usuarios/listar?page=1")

    assert response.status_code == 200
    assert len(response.json()) == 1

    mock_controller.listar_usuarios.assert_called_once_with(1)


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
        user_id=1,   # 🔥 IMPORTANTE (vem do middleware)
        funcional=1,
        campo="usuario_root"
    )


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
        user_id=1,   # 🔥 IMPORTANTE (vem do middleware)
        funcional=1,
        campo="usuario_root"
    )


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


def test_cadastrar_usuario_payload_invalido():
    response = client.post("/usuarios/cadastro", json={
        "usuario": "email-invalido",
        "senha": "123",
        "nome": "J"
    })
    assert response.status_code == 422