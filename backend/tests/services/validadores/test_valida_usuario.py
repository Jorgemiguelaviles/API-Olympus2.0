import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.services.validadores.valida_usuarios import service_validacao_usuario

@pytest.fixture
def service():
    return service_validacao_usuario()

@pytest.fixture
def db_mock():
    return MagicMock()

# ==========================================
# 1. TESTES: CAMPOS OBRIGATÓRIOS
# ==========================================
@pytest.mark.parametrize("campo, payload", [
    ("usuário", {"senha": "Pass123!", "nome": "Jorge"}), # usuário missing
    ("senha", {"usuario": "jorge@itau.com", "nome": "Jorge"}), # senha missing
    ("nome", {"usuario": "jorge@itau.com", "senha": "Pass123!"}), # nome missing
    ("usuário", {"usuario": "  ", "senha": "P1!", "nome": "J"}), # usuário vazio/strip
])
def test_validar_campos_obrigatorios(service, db_mock, campo, payload):
    """Cobre todos os 'if not field or not field.strip()'"""
    with pytest.raises(HTTPException) as exc:
        service.validar(payload, db_mock)
    
    assert exc.value.status_code == 400
    assert f"O campo {campo} é obrigatório" in exc.value.detail

# ==========================================
# 2. TESTE: FORMATO DE EMAIL (REGEX)
# ==========================================
def test_validar_formato_email_invalido(service, db_mock):
    """Cobre o erro de formato de email"""
    payload = {
        "usuario": "email_sem_arroba.com",
        "senha": "Password123!",
        "nome": "Jorge Itau"
    }
    with pytest.raises(HTTPException) as exc:
        service.validar(payload, db_mock)
    
    assert exc.value.status_code == 400
    assert "Formato de email inválido" in exc.value.detail

# ==========================================
# 3. TESTE: SENHA FRACA (REGEX COMPLEXO)
# ==========================================
@pytest.mark.parametrize("senha_fraca", [
    "1234567",       # Curta
    "apenasletras",  # Sem número/especial/maiúscula
    "SemEspecia1",   # Sem caractere especial
    "SEM_MINUSCULA1!", # Sem minúscula
])
def test_validar_senha_fraca(service, db_mock, senha_fraca):
    """Cobre a Regex de senha forte"""
    payload = {
        "usuario": "jorge@itau.com.br",
        "senha": senha_fraca,
        "nome": "Jorge"
    }
    with pytest.raises(HTTPException) as exc:
        service.validar(payload, db_mock)
    
    assert exc.value.status_code == 400
    assert "Senha fraca" in exc.value.detail

# ==========================================
# 4. TESTE: USUÁRIO JÁ EXISTENTE (409)
# ==========================================
def test_validar_usuario_duplicado(service, db_mock):
    """Cobre o erro 409 quando o email já existe no banco"""
    payload = {
        "usuario": "existe@itau.com.br",
        "senha": "Password123!",
        "nome": "Jorge"
    }
    
    # Simula que o banco encontrou um usuário
    db_mock.query.return_value.filter.return_value.first.return_value = MagicMock()
    
    with pytest.raises(HTTPException) as exc:
        service.validar(payload, db_mock)
    
    assert exc.value.status_code == 409
    assert "Usuário já cadastrado" in exc.value.detail

# ==========================================
# 5. TESTE: SUCESSO
# ==========================================
def test_validar_usuario_sucesso(service, db_mock):
    """Cobre o final da função quando tudo está correto"""
    payload = {
        "usuario": "novo_user@itau.com.br",
        "senha": "SafePassword123!",
        "nome": "Jorge Silva"
    }
    
    # Simula que o banco NÃO encontrou usuário (pode retornar None)
    db_mock.query.return_value.filter.return_value.first.return_value = None
    
    # Não deve levantar exceção
    service.validar(payload, db_mock)