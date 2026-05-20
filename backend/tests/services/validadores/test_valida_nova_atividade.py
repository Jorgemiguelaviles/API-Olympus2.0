import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from src.services.validadores.valida_nova_atividade import service_validacao_atividade
from src.models.model_atividades import model_atividades

@pytest.fixture
def service():
    return service_validacao_atividade()

@pytest.fixture
def db_mock():
    return MagicMock()

# ==========================================
# 1. TESTE: DESCRIÇÃO OBRIGATÓRIA (400)
# ==========================================
@pytest.mark.parametrize("descricao_invalida", [None, "", "   "])
def test_validar_cadastro_descricao_obrigatoria(service, db_mock, descricao_invalida):
    """Cobre o erro 400 quando a descrição é nula ou vazia"""
    payload = {"descricao": descricao_invalida}
    
    with pytest.raises(HTTPException) as exc:
        service.validar_cadastro(payload, db_mock)
    
    assert exc.value.status_code == 400
    assert "descrição da atividade é obrigatória" in exc.value.detail

# ==========================================
# 2. TESTE: TAMANHO MÍNIMO (400)
# ==========================================
def test_validar_cadastro_tamanho_minimo(service, db_mock):
    """Cobre o erro 400 quando a descrição tem menos de 3 caracteres"""
    payload = {"descricao": "AB"} # 'AB'.strip() tem len 2
    
    with pytest.raises(HTTPException) as exc:
        service.validar_cadastro(payload, db_mock)
    
    assert exc.value.status_code == 400
    assert "ao menos 3 caracteres" in exc.value.detail

# ==========================================
# 3. TESTE: DUPLICIDADE NO BANCO (409)
# ==========================================
def test_validar_cadastro_duplicidade(service, db_mock):
    """Cobre o erro 409 quando a atividade já existe"""
    payload = {"descricao": "Caminhada"}
    
    # Simula que o banco encontrou um registro
    db_mock.query.return_value.filter.return_value.first.return_value = MagicMock()
    
    with pytest.raises(HTTPException) as exc:
        service.validar_cadastro(payload, db_mock)
    
    assert exc.value.status_code == 409
    assert "já está cadastrada" in exc.value.detail

# ==========================================
# 4. TESTE: SUCESSO E NORMALIZAÇÃO
# ==========================================
def test_validar_cadastro_sucesso(service, db_mock):
    """Cobre o fluxo de sucesso e valida .strip().upper()"""
    payload = {"descricao": "   corrida de rua   "}
    
    # Simula que o banco NÃO encontrou nada
    db_mock.query.return_value.filter.return_value.first.return_value = None
    
    resultado = service.validar_cadastro(payload, db_mock)
    
    # Verifica se limpou os espaços e colocou em caixa alta
    assert resultado["descricao"] == "CORRIDA DE RUA"
    assert db_mock.query.called