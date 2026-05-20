import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from freezegun import freeze_time
from src.services.service_seguranca.limite_login import service_brute_force

@pytest.fixture
def service():
    # Criamos uma nova instância para cada teste para evitar poluição de estado
    return service_brute_force()

def test_registrar_falha_incremento(service):
    """Cobre o incremento do contador de falhas"""
    usuario = "test_user"
    service.registrar_falha(usuario)
    assert service.attempts[usuario]["count"] == 1
    assert service.attempts[usuario]["blocked_until"] is None

@freeze_time("2026-05-20 12:00:00")
def test_bloqueio_apos_max_tentativas(service):
    """Cobre a lógica de bloqueio quando atinge MAX_ATTEMPTS"""
    usuario = "victim"
    # Faz 5 falhas (MAX_ATTEMPTS)
    for _ in range(5):
        service.registrar_falha(usuario)

    # O contador deve resetar e o tempo de bloqueio deve ser +15min
    assert service.attempts[usuario]["count"] == 0
    assert service.attempts[usuario]["blocked_until"] == datetime(2026, 5, 20, 12, 15)

    # Verificar se a exceção 429 é lançada
    with pytest.raises(HTTPException) as exc:
        service.verificar_bloqueio(usuario)
    assert exc.value.status_code == 429
    assert "Muitas tentativas" in exc.value.detail

@freeze_time("2026-05-20 12:00:00")
def test_expiracao_do_bloqueio(service):
    """Cobre o cenário onde o tempo de bloqueio já passou"""
    usuario = "user_expiring"
    
    # Bloqueia o usuário
    for _ in range(5):
        service.registrar_falha(usuario)
    
    # Avança o tempo em 16 minutos (BLOCK_MINUTES + 1)
    with freeze_time("2026-05-20 12:16:00"):
        # Não deve levantar exceção, pois 12:16 > 12:15
        service.verificar_bloqueio(usuario) 

def test_reset_usuario(service):
    """Cobre a função de reset"""
    usuario = "reset_me"
    service.registrar_falha(usuario)
    service.registrar_falha(usuario)
    
    service.reset(usuario)
    
    assert service.attempts[usuario]["count"] == 0
    assert service.attempts[usuario]["blocked_until"] is None

def test_verificar_bloqueio_usuario_limpo(service):
    """Cobre o cenário de um usuário que nunca falhou ou não está bloqueado"""
    # Não deve levantar exceção
    service.verificar_bloqueio("new_user")