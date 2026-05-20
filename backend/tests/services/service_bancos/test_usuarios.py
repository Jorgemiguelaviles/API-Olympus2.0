
# tests/services/test_service_usuarios.py

from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.services.service_bancos.usuarios import (
    service_usuarios
)


# ==========================================
# FIXTURES
# ==========================================
@pytest.fixture
def fake_db():
    return MagicMock()


@pytest.fixture
def service(fake_db):
    return service_usuarios(fake_db)


# ==========================================
# SALVAR USUÁRIO - SUCESSO
# ==========================================
def test_salvar_usuario_sucesso(
    service,
    fake_db
):

    fake_usuario = MagicMock()

    fake_usuario.funcional = 1
    fake_usuario.usuario = "jorge@gmail.com"
    fake_usuario.nome = "Jorge"
    fake_usuario.usuario_root = False
    fake_usuario.usuario_ativado = True

    fake_db.refresh.side_effect = (
        lambda obj: setattr(obj, "funcional", 1)
    )

    payload = {
        "usuario": "jorge@gmail.com",
        "senha_hash": "hash123",
        "nome": "Jorge"
    }

    # mock do model criado
    from src.services.service_bancos import usuarios

    usuarios.model_usuarios = MagicMock(
        return_value=fake_usuario
    )

    resultado = service.salvar(payload)

    assert resultado["funcional"] == 1
    assert resultado["usuario"] == "jorge@gmail.com"
    assert resultado["nome"] == "Jorge"
    assert resultado["usuario_root"] is False
    assert resultado["usuario_ativado"] is True

    fake_db.add.assert_called_once()
    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()


# ==========================================
# SALVAR USUÁRIO - ERRO SQL
# ==========================================
def test_salvar_usuario_sql_error(
    service,
    fake_db
):

    fake_db.commit.side_effect = SQLAlchemyError(
        "Erro banco"
    )

    payload = {
        "usuario": "jorge@gmail.com",
        "senha_hash": "hash123",
        "nome": "Jorge"
    }

    with pytest.raises(Exception) as erro:

        service.salvar(payload)

    assert "Erro ao salvar usuário no banco" in str(
        erro.value
    )

    fake_db.rollback.assert_called_once()


# ==========================================
# LISTAR USUÁRIOS
# ==========================================
def test_listar_usuarios(
    service,
    fake_db
):

    usuario = MagicMock()

    usuario.funcional = 1
    usuario.usuario = "jorge@gmail.com"
    usuario.nome = "Jorge"
    usuario.usuario_root = False
    usuario.usuario_ativado = True

    (
        fake_db.query.return_value
        .offset.return_value
        .limit.return_value
        .all.return_value
    ) = [usuario]

    resultado = service.listar_usuarios(1)

    assert resultado == [
        {
            "funcional": 1,
            "usuario": "jorge@gmail.com",
            "nome": "Jorge",
            "usuario_root": False,
            "usuario_ativado": True
        }
    ]


# ==========================================
# LISTAR USUÁRIOS - PAGE < 1
# ==========================================
def test_listar_usuarios_page_menor_que_um(
    service,
    fake_db
):

    (
        fake_db.query.return_value
        .offset.return_value
        .limit.return_value
        .all.return_value
    ) = []

    resultado = service.listar_usuarios(0)

    assert resultado == []

    fake_db.query.return_value.offset.assert_called_once_with(
        0
    )


# ==========================================
# ALTERAR CONFIGURAÇÃO - SUCESSO
# ==========================================
def test_alterar_configuracao_usuario(
    service,
    fake_db
):

    usuario = MagicMock()

    usuario.funcional = 1
    usuario.usuario_root = False

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = usuario

    resultado = service.alterar_configuracao_usuario(
        1,
        "usuario_root"
    )

    assert resultado == {
        "message": "usuario_root atualizado com sucesso.",
        "funcional": 1,
        "usuario_root": True
    }

    assert usuario.usuario_root is True

    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()


# ==========================================
# ALTERAR CONFIGURAÇÃO - ERRO SQL
# ==========================================
def test_alterar_configuracao_usuario_sql_error(
    service,
    fake_db
):

    usuario = MagicMock()

    usuario.usuario_root = False

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = usuario

    fake_db.commit.side_effect = SQLAlchemyError(
        "Erro banco"
    )

    with pytest.raises(Exception) as erro:

        service.alterar_configuracao_usuario(
            1,
            "usuario_root"
        )

    assert (
        "Erro ao alterar configuração do usuário"
        in str(erro.value)
    )

    fake_db.rollback.assert_called_once()


# ==========================================
# ATUALIZAR USUÁRIO - SUCESSO
# ==========================================
def test_atualizar_usuario_sucesso(
    service,
    fake_db
):

    usuario = MagicMock()

    usuario.funcional = 1
    usuario.usuario = "jorge@gmail.com"
    usuario.nome = "Jorge"
    usuario.usuario_root = False
    usuario.usuario_ativado = True

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = usuario

    payload = {
        "nome": "Jorge Miguel",
        "usuario": "novo@gmail.com",
        "senha_hash": None
    }

    resultado = service.atualizar_usuario(
        1,
        payload
    )

    assert resultado == {
        "funcional": 1,
        "usuario": "novo@gmail.com",
        "nome": "Jorge Miguel",
        "usuario_root": False,
        "usuario_ativado": True
    }

    fake_db.commit.assert_called_once()
    fake_db.refresh.assert_called_once()


# ==========================================
# ATUALIZAR USUÁRIO - IGNORA NONE
# ==========================================
def test_atualizar_usuario_ignora_none(
    service,
    fake_db
):

    usuario = MagicMock()

    usuario.funcional = 1
    usuario.usuario = "jorge@gmail.com"
    usuario.nome = "Jorge"
    usuario.usuario_root = False
    usuario.usuario_ativado = True

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = usuario

    payload = {
        "nome": None
    }

    resultado = service.atualizar_usuario(
        1,
        payload
    )

    assert resultado["nome"] == "Jorge"


# ==========================================
# ATUALIZAR USUÁRIO - ERRO SQL
# ==========================================
def test_atualizar_usuario_sql_error(
    service,
    fake_db
):

    usuario = MagicMock()

    (
        fake_db.query.return_value
        .filter.return_value
        .first.return_value
    ) = usuario

    fake_db.commit.side_effect = SQLAlchemyError(
        "Erro banco"
    )

    with pytest.raises(Exception) as erro:

        service.atualizar_usuario(
            1,
            {"nome": "Novo Nome"}
        )

    assert "Erro ao atualizar usuário" in str(
        erro.value
    )

    fake_db.rollback.assert_called_once()
