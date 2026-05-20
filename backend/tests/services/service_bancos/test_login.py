# tests/services/test_service_login.py

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.services.service_bancos.login import (
    service_login
)


# ==========================================
# MOCK USER
# ==========================================
class FakeUser:

    def __init__(
        self,
        funcional=1,
        usuario="jorge@gmail.com",
        nome="Jorge",
        usuario_root=False,
        usuario_ativado=True,
        senha_hash="hash"
    ):

        self.funcional = funcional
        self.usuario = usuario
        self.nome = nome
        self.usuario_root = usuario_root
        self.usuario_ativado = usuario_ativado
        self.senha_hash = senha_hash


# ==========================================
# SERVICE
# ==========================================
def criar_service(user=None):

    db = MagicMock()

    query = (
        db.query.return_value
        .filter.return_value
    )

    query.first.return_value = user

    return service_login(db)


# ==========================================
# LOGIN SUCESSO
# ==========================================
@patch(
    "src.services.service_bancos.login.CryptContext.verify"
)
def test_autenticar_sucesso(
    mock_verify
):

    mock_verify.return_value = True

    user = FakeUser()

    service = criar_service(user)

    resultado = service.autenticar(
        "jorge@gmail.com",
        "123456"
    )

    assert resultado["funcional"] == 1

    assert resultado["usuario"] == (
        "jorge@gmail.com"
    )

    assert resultado["nome"] == "Jorge"

    assert resultado["usuario_root"] is False

    assert resultado["usuario_ativado"] is True


# ==========================================
# USUÁRIO NÃO EXISTE
# ==========================================
def test_autenticar_usuario_inexistente():

    service = criar_service(None)

    with pytest.raises(HTTPException) as erro:

        service.autenticar(
            "fake@gmail.com",
            "123456"
        )

    assert erro.value.status_code == 401

    assert (
        erro.value.detail
        == "Usuário ou senha inválidos."
    )


# ==========================================
# USUÁRIO DESATIVADO
# ==========================================
def test_autenticar_usuario_desativado():

    user = FakeUser(
        usuario_ativado=False
    )

    service = criar_service(user)

    with pytest.raises(HTTPException) as erro:

        service.autenticar(
            "jorge@gmail.com",
            "123456"
        )

    assert erro.value.status_code == 403

    assert (
        erro.value.detail
        == "Usuário desativado. Entre em contato com o suporte."
    )


# ==========================================
# SENHA INVÁLIDA
# ==========================================
@patch(
    "src.services.service_bancos.login.CryptContext.verify"
)
def test_autenticar_senha_invalida(
    mock_verify
):

    mock_verify.return_value = False

    user = FakeUser()

    service = criar_service(user)

    with pytest.raises(HTTPException) as erro:

        service.autenticar(
            "jorge@gmail.com",
            "senha_errada"
        )

    assert erro.value.status_code == 401

    assert (
        erro.value.detail
        == "Usuário ou senha inválidos."
    )


# ==========================================
# VERIFY CHAMADO
# ==========================================
@patch(
    "src.services.service_bancos.login.CryptContext.verify"
)
def test_verify_called(
    mock_verify
):

    mock_verify.return_value = True

    user = FakeUser()

    service = criar_service(user)

    service.autenticar(
        "jorge@gmail.com",
        "123456"
    )

    mock_verify.assert_called_once_with(
        "123456",
        "hash"
    )