import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, Request
from jose import jwt
import os

# Mock do arquivo de chave pública antes de importar o middleware
# Isso evita erros de "file not found" durante o import
with patch("builtins.open", MagicMock()):
    with patch("os.getenv", return_value="fake_path"):
        from src.middlewares.bearer import AuthMiddleware

@pytest.fixture
def middleware():
    # app=None pois o middleware será testado isoladamente chamando .dispatch()
    return AuthMiddleware(app=None)

@pytest.fixture
def mock_call_next():
    async def call_next(request):
        return "Sucesso"
    return call_next

def create_mock_request(path, method="GET", headers=None):
    request = MagicMock(spec=Request)
    request.url.path = path
    request.method = method
    request.headers = headers or {}
    request.state = MagicMock()
    return request

# ==========================================
# 1. TESTE: ROTA PÚBLICA (Sucesso)
# ==========================================
@pytest.mark.asyncio
async def test_auth_public_route(middleware, mock_call_next):
    request = create_mock_request("/usuarios/login")
    response = await middleware.dispatch(request, mock_call_next)
    assert response == "Sucesso"

# ==========================================
# 2. TESTE: TOKEN AUSENTE (401)
# ==========================================
@pytest.mark.asyncio
async def test_auth_token_ausente(middleware, mock_call_next):
    request = create_mock_request("/atividadespraticadas", headers={})
    with pytest.raises(HTTPException) as exc:
        await middleware.dispatch(request, mock_call_next)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Token ausente"

# ==========================================
# 3. TESTE: FORMATO INVÁLIDO / SPLIT (401)
# ==========================================
@pytest.mark.asyncio
@pytest.mark.parametrize("auth_header", ["Bearer", "Basic 123", "Bearer-token-sem-espaco"])
async def test_auth_header_invalido(middleware, mock_call_next, auth_header):
    request = create_mock_request("/atividadespraticadas", headers={"Authorization": auth_header})
    with pytest.raises(HTTPException) as exc:
        await middleware.dispatch(request, mock_call_next)
    assert exc.value.status_code == 401

# ==========================================
# 4. TESTE: TOKEN INVÁLIDO OU EXPIRADO (401)
# ==========================================
@pytest.mark.asyncio
async def test_auth_token_decodificacao_falha(middleware, mock_call_next):
    request = create_mock_request("/atividadespraticadas", headers={"Authorization": "Bearer token_podre"})
    
    with patch("jose.jwt.decode", side_effect=Exception("Erro JWT")):
        with pytest.raises(HTTPException) as exc:
            await middleware.dispatch(request, mock_call_next)
    
    assert exc.value.status_code == 401
    assert exc.value.detail == "Token inválido"

# ==========================================
# 5. TESTE: USUÁRIO DESATIVADO (403)
# ==========================================
@pytest.mark.asyncio
async def test_auth_usuario_desativado(middleware, mock_call_next):
    request = create_mock_request("/atividadespraticadas", headers={"Authorization": "Bearer token"})
    payload = {"usuario_ativado": False}
    
    with patch("jose.jwt.decode", return_value=payload):
        with pytest.raises(HTTPException) as exc:
            await middleware.dispatch(request, mock_call_next)
    
    assert exc.value.status_code == 403
    assert exc.value.detail == "Usuário desativado"

# ==========================================
# 6. TESTE: ROOT LIBERADO (Sucesso)
# ==========================================
@pytest.mark.asyncio
async def test_auth_root_access(middleware, mock_call_next):
    request = create_mock_request("/rota/qualquer", headers={"Authorization": "Bearer token"})
    payload = {"usuario_ativado": True, "usuario_root": True}
    
    with patch("jose.jwt.decode", return_value=payload):
        response = await middleware.dispatch(request, mock_call_next)
    
    assert response == "Sucesso"
    assert request.state.user == payload

# ==========================================
# 7. TESTE: USER COMUM - ROTA PERMITIDA (Sucesso)
# ==========================================
@pytest.mark.asyncio
@pytest.mark.parametrize("method, path", [
    ("POST", "/atividadespraticadas"),
    ("GET", "/atividades/opcoes"),
    ("GET", "/atividadespraticadas/123") # Rota dinâmica
])
async def test_auth_user_comum_permitido(middleware, mock_call_next, method, path):
    request = create_mock_request(path, method=method, headers={"Authorization": "Bearer token"})
    payload = {"usuario_ativado": True, "usuario_root": False}
    
    with patch("jose.jwt.decode", return_value=payload):
        response = await middleware.dispatch(request, mock_call_next)
    
    assert response == "Sucesso"

# ==========================================
# 8. TESTE: USER COMUM - ACESSO NEGADO (403)
# ==========================================
@pytest.mark.asyncio
async def test_auth_user_comum_negado(middleware, mock_call_next):
    request = create_mock_request("/usuarios", method="GET", headers={"Authorization": "Bearer token"})
    payload = {"usuario_ativado": True, "usuario_root": False}
    
    with patch("jose.jwt.decode", return_value=payload):
        with pytest.raises(HTTPException) as exc:
            await middleware.dispatch(request, mock_call_next)
    
    assert exc.value.status_code == 403
    assert "Acesso negado" in exc.value.detail