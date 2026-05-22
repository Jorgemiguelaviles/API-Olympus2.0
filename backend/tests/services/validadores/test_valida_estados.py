import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from src.services.validadores.valida_estados import service_validacao_estados

# Fixture para instanciar o serviço antes de cada teste
@pytest.fixture
def service():
    return service_validacao_estados()

# Fixture para mockar o banco de dados
@pytest.fixture
def db_mock():
    return MagicMock()


def test_validar_usuario_inexistente(service, db_mock):
    # Configura o mock do banco para retornar None (usuário não encontrado)
    db_mock.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        # Passando user_id=1 operando sobre funcional=999 (não existe)
        service.validar(user_id=1, funcional=999, campo="usuario_root", db=db_mock)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Usuário não encontrado."


def test_validar_alteracao_propria_proibida(service, db_mock):
    # Mock do usuário retornado
    usuario_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = usuario_mock

    with pytest.raises(HTTPException) as exc_info:
        # user_id igual ao funcional (tentando alterar a si mesmo)
        service.validar(user_id=12345, funcional=12345, campo="usuario_root", db=db_mock)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Usuário não pode alterar o próprio estado."


def test_validar_campo_proibido(service, db_mock):
    # Mock do usuário retornado
    usuario_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = usuario_mock

    with pytest.raises(HTTPException) as exc_info:
        # user_id=1 alterando funcional=999 (permitido), mas com campo inválido
        service.validar(user_id=1, funcional=999, campo="campo_invalido_qualquer", db=db_mock)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Campo inválido para alteração."


@pytest.mark.parametrize("campo_valido", ["usuario_root", "usuario_ativado"])
def test_validar_sucesso(service, db_mock, campo_valido):
    # Mock do usuário retornado
    usuario_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = usuario_mock

    # user_id=1 alterando funcional=999 (diferentes), com campos permitidos
    resultado = service.validar(user_id=1, funcional=999, campo=campo_valido, db=db_mock)

    assert resultado == usuario_mock