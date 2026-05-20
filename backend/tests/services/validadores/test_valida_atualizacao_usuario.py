import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.services.validadores.valida_atualizacao_usuario import service_validacao_atualizacao_usuario

@pytest.fixture
def service():
    return service_validacao_atualizacao_usuario()

@pytest.fixture
def db_mock():
    return MagicMock()

# ==========================================
# TESTES DE FUNCIONAL
# ==========================================

def test_validar_funcional_ausente(service, db_mock):
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes({}, db_mock)
    assert exc.value.status_code == 400
    assert "Funcional é obrigatória" in exc.value.detail

def test_validar_funcional_nao_numerica(service, db_mock):
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes({"funcional": "abc"}, db_mock)
    assert exc.value.status_code == 400
    assert "deve ser numérica" in exc.value.detail

def test_validar_usuario_nao_encontrado(service, db_mock):
    db_mock.query.return_value.filter.return_value.first.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes({"funcional": "123"}, db_mock)
    assert exc.value.status_code == 404

# ==========================================
# TESTES DE NOME
# ==========================================

def test_validar_nome_curto(service, db_mock):
    db_mock.query.return_value.filter.return_value.first.return_value = True # Usuario existe
    payload = {"funcional": "123", "nome": "Jo"}
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes(payload, db_mock)
    assert exc.value.status_code == 400
    assert "ao menos 3 caracteres" in exc.value.detail

# ==========================================
# TESTES DE EMAIL (USUARIO)
# ==========================================

def test_validar_email_invalido(service, db_mock):
    db_mock.query.return_value.filter.return_value.first.return_value = True
    payload = {"funcional": "123", "usuario": "email_errado"}
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes(payload, db_mock)
    assert exc.value.status_code == 400
    assert "Formato de email inválido" in exc.value.detail

def test_validar_email_ja_cadastrado(service, db_mock):
    # Simula usuario existe, mas depois simula que o email pertence a OUTRA funcional
    db_mock.query.return_value.filter.return_value.first.side_effect = [True, True]
    payload = {"funcional": "123", "usuario": "teste@itau.com.br"}
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes(payload, db_mock)
    assert "Email já cadastrado" in exc.value.detail

# ==========================================
# TESTES DE SENHA
# ==========================================

def test_validar_senha_fraca(service, db_mock):
    db_mock.query.return_value.filter.return_value.first.return_value = True
    payload = {"funcional": "123", "senha": "123"}
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes(payload, db_mock)
    assert "Senha fraca" in exc.value.detail

# ==========================================
# TESTES DE SUCESSO E NADA ENVIADO
# ==========================================

def test_validar_nada_enviado(service, db_mock):
    db_mock.query.return_value.filter.return_value.first.return_value = True
    payload = {"funcional": "123"} # Só a funcional, sem campos de update
    with pytest.raises(HTTPException) as exc:
        service.validar_atualizacoes(payload, db_mock)
    assert "Nenhum campo enviado" in exc.value.detail

def test_validar_sucesso_completo(service, db_mock):
    # Mock para usuario existe (123) e email não está em uso por outros
    db_mock.query.return_value.filter.return_value.first.side_effect = [True, None]
    
    payload = {
        "funcional": "123",
        "nome": " Jorge Itau ",
        "usuario": "jorge@itau.com.br",
        "senha": "Password123!"
    }
    
    res = service.validar_atualizacoes(payload, db_mock)
    
    assert res["nome"] == "Jorge Itau" # Verifica o strip()
    assert res["usuario"] == "jorge@itau.com.br"
    assert "senha" in res