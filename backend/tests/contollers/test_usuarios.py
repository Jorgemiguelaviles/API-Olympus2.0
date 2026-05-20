# tests/controllers/test_controller_usuarios.py

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.contollers.controller_usuarios import (
    controller_usuarios
)


# ==========================================
# FIXTURE
# ==========================================
@pytest.fixture
def db_mock():
    return MagicMock()


# ==========================================
# INIT
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_init_controller(
    mock_login_service,
    mock_usuario_service,
    db_mock
):

    controller = controller_usuarios(db_mock)

    assert controller.db == db_mock
    assert controller.usuario_service is not None
    assert controller.login_service is not None
    assert controller.brute_force is not None
    assert controller.pwd_context is not None


# ==========================================
# CADASTRAR USUÁRIO - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_usuario"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_cadastrar_usuario_sucesso(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    usuario_salvo = {
        "funcional": 1,
        "usuario": "jorge@gmail.com"
    }

    service_instance = MagicMock()

    service_instance.salvar.return_value = usuario_salvo

    mock_usuario_service.return_value = service_instance

    validacao_instance = MagicMock()

    mock_validacao.return_value = validacao_instance

    controller = controller_usuarios(db_mock)

    payload = {
        "usuario": "jorge@gmail.com",
        "senha": "123456",
        "nome": "Jorge"
    }

    resultado = controller.cadastrar_usuario(
        payload
    )

    assert resultado == usuario_salvo

    validacao_instance.validar.assert_called_once_with(
        payload,
        db_mock
    )

    service_instance.salvar.assert_called_once()

    payload_salvo = (
        service_instance.salvar.call_args[0][0]
    )

    assert payload_salvo["usuario"] == (
        "jorge@gmail.com"
    )

    assert payload_salvo["nome"] == "Jorge"

    assert "senha_hash" in payload_salvo

    assert payload_salvo["senha_hash"] != "123456"


# ==========================================
# CADASTRAR USUÁRIO - HTTPException
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_usuario"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_cadastrar_usuario_http_exception(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    validacao_instance = MagicMock()

    validacao_instance.validar.side_effect = (
        HTTPException(
            status_code=409,
            detail="Usuário já existe"
        )
    )

    mock_validacao.return_value = validacao_instance

    controller = controller_usuarios(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.cadastrar_usuario({
            "usuario": "jorge@gmail.com",
            "senha": "123456",
            "nome": "Jorge"
        })

    assert erro.value.status_code == 409


# ==========================================
# CADASTRAR USUÁRIO - ERRO INTERNO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_usuario"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_cadastrar_usuario_erro_interno(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    validacao_instance = MagicMock()

    mock_validacao.return_value = validacao_instance

    service_instance = MagicMock()

    service_instance.salvar.side_effect = (
        Exception("Falha banco")
    )

    mock_usuario_service.return_value = service_instance

    controller = controller_usuarios(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.cadastrar_usuario({
            "usuario": "jorge@gmail.com",
            "senha": "123456",
            "nome": "Jorge"
        })

    assert erro.value.status_code == 500

    assert (
        "Erro interno ao cadastrar usuário"
        in erro.value.detail
    )


# ==========================================
# LISTAR USUÁRIOS - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_listar_usuarios_sucesso(
    mock_login_service,
    mock_usuario_service,
    db_mock
):

    usuarios_mock = [
        {
            "funcional": 1,
            "usuario": "jorge@gmail.com"
        }
    ]

    service_instance = MagicMock()

    service_instance.listar_usuarios.return_value = (
        usuarios_mock
    )

    mock_usuario_service.return_value = service_instance

    controller = controller_usuarios(db_mock)

    resultado = controller.listar_usuarios(1)

    assert resultado == usuarios_mock

    service_instance.listar_usuarios.assert_called_once_with(
        1
    )


# ==========================================
# LISTAR USUÁRIOS - ERRO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_listar_usuarios_erro(
    mock_login_service,
    mock_usuario_service,
    db_mock
):

    service_instance = MagicMock()

    service_instance.listar_usuarios.side_effect = (
        Exception("Falha")
    )

    mock_usuario_service.return_value = service_instance

    controller = controller_usuarios(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.listar_usuarios(1)

    assert erro.value.status_code == 500


# ==========================================
# LOGIN - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.create_access_token"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_login_sucesso(
    mock_login_service_class,
    mock_usuario_service,
    mock_create_token,
    db_mock
):

    user_mock = {
        "funcional": 1,
        "usuario": "jorge@gmail.com",
        "nome": "Jorge",
        "usuario_root": False,
        "usuario_ativado": True
    }

    login_instance = MagicMock()

    login_instance.autenticar.return_value = (
        user_mock
    )

    mock_login_service_class.return_value = (
        login_instance
    )

    mock_create_token.return_value = "token_fake"

    controller = controller_usuarios(db_mock)

    controller.brute_force = MagicMock()

    resultado = controller.login({
        "usuario": "jorge@gmail.com",
        "senha": "123456"
    })

    assert resultado == {
        "access_token": "token_fake",
        "token_type": "bearer"
    }

    controller.brute_force.verificar_bloqueio.assert_called_once()

    controller.brute_force.reset.assert_called_once()

    login_instance.autenticar.assert_called_once()


# ==========================================
# LOGIN - HTTPException
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_login_http_exception(
    mock_login_service_class,
    mock_usuario_service,
    db_mock
):

    login_instance = MagicMock()

    login_instance.autenticar.side_effect = (
        HTTPException(
            status_code=401,
            detail="Credenciais inválidas"
        )
    )

    mock_login_service_class.return_value = (
        login_instance
    )

    controller = controller_usuarios(db_mock)

    controller.brute_force = MagicMock()

    with pytest.raises(HTTPException) as erro:

        controller.login({
            "usuario": "jorge@gmail.com",
            "senha": "123456"
        })

    assert erro.value.status_code == 401

    controller.brute_force.registrar_falha.assert_called_once()


# ==========================================
# LOGIN - ERRO INTERNO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_login_erro_interno(
    mock_login_service_class,
    mock_usuario_service,
    db_mock
):

    login_instance = MagicMock()

    login_instance.autenticar.side_effect = (
        Exception("Falha login")
    )

    mock_login_service_class.return_value = (
        login_instance
    )

    controller = controller_usuarios(db_mock)

    controller.brute_force = MagicMock()

    with pytest.raises(HTTPException) as erro:

        controller.login({
            "usuario": "jorge@gmail.com",
            "senha": "123456"
        })

    assert erro.value.status_code == 500

    assert (
        "Erro interno no login"
        in erro.value.detail
    )


# ==========================================
# ALTERAR CONFIGURAÇÃO - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_estados"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_alterar_configuracao_sucesso(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    retorno_mock = {
        "status": "ok"
    }

    service_instance = MagicMock()

    service_instance.alterar_configuracao_usuario.return_value = (
        retorno_mock
    )

    mock_usuario_service.return_value = service_instance

    validacao_instance = MagicMock()

    mock_validacao.return_value = validacao_instance

    controller = controller_usuarios(db_mock)

    resultado = controller.alterar_configuracao_usuario(
        1,
        "usuario_root"
    )

    assert resultado == retorno_mock

    validacao_instance.validar.assert_called_once_with(
        1,
        "usuario_root",
        db_mock
    )


# ==========================================
# ALTERAR CONFIGURAÇÃO - ERRO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_estados"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_alterar_configuracao_erro(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    validacao_instance = MagicMock()

    validacao_instance.validar.side_effect = (
        Exception("Falha")
    )

    mock_validacao.return_value = validacao_instance

    controller = controller_usuarios(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.alterar_configuracao_usuario(
            1,
            "usuario_root"
        )

    assert erro.value.status_code == 500


# ==========================================
# ATUALIZAR USUÁRIO - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_atualizacao_usuario"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_atualizar_usuario_sucesso(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    dados_mock = {
        "nome": "Jorge",
        "senha": "123456"
    }

    retorno_mock = {
        "status": "ok"
    }

    validacao_instance = MagicMock()

    validacao_instance.validar_atualizacoes.return_value = (
        dados_mock
    )

    mock_validacao.return_value = validacao_instance

    service_instance = MagicMock()

    service_instance.atualizar_usuario.return_value = (
        retorno_mock
    )

    mock_usuario_service.return_value = service_instance

    controller = controller_usuarios(db_mock)

    resultado = controller.atualizar_usuario(
        1,
        {"nome": "Jorge"}
    )

    assert resultado == retorno_mock

    payload_enviado = (
        service_instance.atualizar_usuario.call_args[0][1]
    )

    assert "senha_hash" in payload_enviado

    assert "senha" not in payload_enviado


# ==========================================
# ATUALIZAR USUÁRIO - HTTPException
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_atualizacao_usuario"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_atualizar_usuario_http_exception(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    validacao_instance = MagicMock()

    validacao_instance.validar_atualizacoes.side_effect = (
        HTTPException(
            status_code=400,
            detail="Payload inválido"
        )
    )

    mock_validacao.return_value = validacao_instance

    controller = controller_usuarios(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.atualizar_usuario(
            1,
            {}
        )

    assert erro.value.status_code == 400


# ==========================================
# ATUALIZAR USUÁRIO - ERRO INTERNO
# ==========================================
@patch(
    "src.contollers.controller_usuarios.service_validacao_atualizacao_usuario"
)
@patch(
    "src.contollers.controller_usuarios.service_usuarios"
)
@patch(
    "src.contollers.controller_usuarios.service_login"
)
def test_atualizar_usuario_erro(
    mock_login_service,
    mock_usuario_service,
    mock_validacao,
    db_mock
):

    validacao_instance = MagicMock()

    validacao_instance.validar_atualizacoes.side_effect = (
        Exception("Falha update")
    )

    mock_validacao.return_value = validacao_instance

    controller = controller_usuarios(db_mock)

    with pytest.raises(HTTPException) as erro:

        controller.atualizar_usuario(
            1,
            {}
        )

    assert erro.value.status_code == 500

    assert (
        "Erro ao atualizar usuário"
        in erro.value.detail
    )