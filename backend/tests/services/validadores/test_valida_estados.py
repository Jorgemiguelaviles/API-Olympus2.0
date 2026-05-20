import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.services.validadores.valida_estados import service_validacao_estados
from src.models.model_usuarios import model_usuarios

@pytest.fixture
def service():
    return service_validacao_estados()

@pytest.fixture
def db_mock():
    return MagicMock()

# ==========================================
# TESTE: USUÁRIO NÃO ENCONTRADO
# ==========================================
def test_validar_usuario_inexistente(service, db_mock):
    """Cobre o erro 404 quando o funcional não existe no banco"""
    # db.query().filter().first() -> None
    db_mock.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(HTTPException) as exc:
        service.validar(funcional=12345, campo="usuario_root", db=db_mock)
    
    assert exc.value.status_code == 404
    assert exc.value.detail == "Usuário não encontrado."

# ==========================================
# TESTE: CAMPO INVÁLIDO
# ==========================================
def test_validar_campo_proibido(service, db_mock):
    """Cobre o erro 400 quando o campo não está em CAMPOS_PERMITIDOS"""
    # Simula que o usuário EXISTE
    usuario_mock = model_usuarios(funcional=12345)
    db_mock.query.return_value.filter.return_value.first.return_value = usuario_mock
    
    with pytest.raises(HTTPException) as exc:
        # 'senha' não está na lista CAMPOS_PERMITIDOS
        service.validar(funcional=12345, campo="senha", db=db_mock)
    
    assert exc.value.status_code == 400
    assert exc.value.detail == "Campo inválido para alteração."

# ==========================================
# TESTE: SUCESSO
# ==========================================
def test_validar_sucesso(service, db_mock):
    """Cobre o fluxo de sucesso retornando o objeto usuário"""
    usuario_mock = model_usuarios(funcional=999)
    db_mock.query.return_value.filter.return_value.first.return_value = usuario_mock
    
    # Testa os dois campos permitidos
    for campo in ["usuario_root", "usuario_ativado"]:
        resultado = service.validar(funcional=999, campo=campo, db=db_mock)
        assert resultado == usuario_mock