import pytest
import time
from unittest.mock import patch, mock_open
from jose import jwt

# Simulamos a chave privada para não depender de arquivos do sistema
FAKE_PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA7..." # Abreviação
ALGORITHM = "RS256"

# Mockando o open e o load_dotenv ANTES de importar o seu módulo
with patch("builtins.open", mock_open(read_data=FAKE_PRIVATE_KEY)), \
     patch("os.getenv", return_value="fake_path.pem"):
    from src.services.service_seguranca.jwt import create_access_token, PRIVATE_KEY

def test_create_access_token_success():
    """Testa se o token é gerado com os campos corretos no payload"""
    data = {"sub": "user123", "usuario_root": True}
    token = create_access_token(data)
    
    assert isinstance(token, str)
    
    # Decodificamos sem verificar assinatura (apenas para validar o conteúdo do payload)
    # Nota: Em um teste real, você usaria a PUBLIC_KEY correspondente
    unverified_payload = jwt.get_unverified_claims(token)
    
    assert unverified_payload["sub"] == "user123"
    assert unverified_payload["usuario_root"] is True
    assert "iat" in unverified_payload
    assert "exp" in unverified_payload

def test_token_expiration_logic():
    """Valida se o tempo de expiração é exatamente 60 minutos após o iat"""
    data = {"sub": "test"}
    token = create_access_token(data)
    payload = jwt.get_unverified_claims(token)
    
    iat = payload["iat"]
    exp = payload["exp"]
    
    # Diferença deve ser de 3600 segundos (60 min * 60s)
    assert exp - iat == 3600

def test_token_iat_is_current_time():
    """Valida se o iat reflete o timestamp atual (margem de erro de 2s)"""
    now = int(time.time())
    token = create_access_token({"sub": "time_test"})
    payload = jwt.get_unverified_claims(token)
    
    assert abs(payload["iat"] - now) <= 2

def test_create_token_empty_dict():
    """Garante que funciona mesmo com dicionário vazio (apenas iat/exp)"""
    token = create_access_token({})
    payload = jwt.get_unverified_claims(token)
    
    assert "iat" in payload
    assert "exp" in payload