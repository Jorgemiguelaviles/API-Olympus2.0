import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from src.contollers.controller_usuarios import controller_usuarios


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def controller(mock_db):
    # Patch na inicialização dos serviços internos para não depender do banco real
    with patch('src.contollers.controller_usuarios.service_usuarios'), \
         patch('src.contollers.controller_usuarios.service_login'), \
         patch('src.contollers.controller_usuarios.brute_force_instance'):
        
        ctrl = controller_usuarios(db=mock_db)
        # Substitui os atributos por mocks limpos para asserções precisas
        ctrl.usuario_service = MagicMock()
        ctrl.login_service = MagicMock()
        ctrl.brute_force = MagicMock()
        return ctrl


# ==============================================================================
# TESTES: CADASTRAR USUÁRIO
# ==============================================================================

@patch('src.contollers.controller_usuarios.service_validacao_usuario')
def test_cadastrar_usuario_sucesso(mock_validador, controller):
    """Deve cadastrar um usuário com sucesso gerando o hash da senha."""
    payload = {"usuario": "testuser", "senha": "secret_password", "nome": "Test"}
    controller.usuario_service.salvar.return_value = {"id": 1, "usuario": "testuser"}

    resultado = controller.cadastrar_usuario(payload)

    assert resultado == {"id": 1, "usuario": "testuser"}
    controller.usuario_service.salvar.assert_called_once()
    # Garante que a senha salva passou por criptografia e não está em texto plano
    dict_salvo = controller.usuario_service.salvar.call_args[0][0]
    assert dict_salvo["senha_hash"] != "secret_password"


@patch('src.contollers.controller_usuarios.service_validacao_usuario')
def test_cadastrar_usuario_erro_validacao(mock_validador, controller):
    """Deve repassar a HTTPException lançada pelo validador sem alteração."""
    mock_instancia = mock_validador.return_value
    mock_instancia.validar.side_effect = HTTPException(status_code=400, detail="Usuário inválido")

    with pytest.raises(HTTPException) as exc_info:
        controller.cadastrar_usuario({"usuario": "invalido"})
    
    assert exc_info.value.status_code == 400


@patch('src.contollers.controller_usuarios.service_validacao_usuario')
def test_cadastrar_usuario_erro_interno(mock_validador, controller):
    """Deve capturar qualquer erro inesperado e converter em HTTPException 500."""
    controller.usuario_service.salvar.side_effect = Exception("Crash no banco de dados")

    with pytest.raises(HTTPException) as exc_info:
        controller.cadastrar_usuario({"usuario": "testuser", "senha": "123"})
    
    assert exc_info.value.status_code == 500
    assert "Erro interno ao cadastrar usuário" in exc_info.value.detail


# ==============================================================================
# TESTES: LISTAR USUÁRIOS
# ==============================================================================

def test_listar_usuarios_sucesso(controller):
    """Deve retornar a listagem de usuários paginada corretamente."""
    controller.usuario_service.listar_usuarios.return_value = [{"id": 1, "nome": "User 1"}]

    resultado = controller.listar_usuarios(page=1)

    assert resultado == [{"id": 1, "nome": "User 1"}]
    controller.usuario_service.listar_usuarios.assert_called_once_with(1)


def test_listar_usuarios_erro_interno(controller):
    """Deve converter falhas na listagem de usuários em erro HTTP 500."""
    controller.usuario_service.listar_usuarios.side_effect = Exception("Timeout")

    with pytest.raises(HTTPException) as exc_info:
        controller.listar_usuarios(page=1)
    
    assert exc_info.value.status_code == 500
    assert "Erro ao listar usuários" in exc_info.value.detail


# ==============================================================================
# TESTES: LOGIN
# ==============================================================================

@patch('src.contollers.controller_usuarios.create_access_token')
def test_login_sucesso(mock_jwt, controller):
    """Deve autenticar com sucesso, limpar histórico de brute force e retornar o token JWT."""
    payload = {"usuario": "jorge", "senha": "password123"}
    user_mock = {
        "funcional": 12345, "usuario": "jorge", "nome": "Jorge",
        "usuario_root": False, "usuario_ativado": True
    }
    controller.login_service.autenticar.return_value = user_mock
    mock_jwt.return_value = "mocked_jwt_string"

    resultado = controller.login(payload)

    assert resultado == {"access_token": "mocked_jwt_string", "token_type": "bearer"}
    controller.brute_force.verificar_bloqueio.assert_called_once_with("jorge")
    controller.brute_force.reset.assert_called_once_with("jorge")


def test_login_falha_autenticacao(controller):
    """Deve registrar a falha de tentativa no brute force quando as credenciais estiverem erradas."""
    payload = {"usuario": "jorge", "senha": "senha_errada"}
    controller.login_service.autenticar.side_effect = HTTPException(status_code=401, detail="Senha incorreta")

    with pytest.raises(HTTPException) as exc_info:
        controller.login(payload)
    
    assert exc_info.value.status_code == 401
    controller.brute_force.registrar_falha.assert_called_once_with("jorge")


def test_login_erro_interno(controller):
    """Deve retornar erro 500 caso ocorra alguma falha sistêmica durante o login."""
    payload = {"usuario": "jorge", "senha": "password123"}
    controller.brute_force.verificar_bloqueio.side_effect = Exception("Redis offline")

    with pytest.raises(HTTPException) as exc_info:
        controller.login(payload)
    
    assert exc_info.value.status_code == 500
    assert "Erro interno no login" in exc_info.value.detail


# ==============================================================================
# TESTES: ALTERAR CONFIGURAÇÃO USUÁRIO
# ==============================================================================

@patch('src.contollers.controller_usuarios.service_validacao_estados')
def test_alterar_configuracao_usuario_sucesso(mock_validador, controller):
    """Deve aplicar a alteração de configuração após validação bem-sucedida."""
    controller.usuario_service.alterar_configuracao_usuario.return_value = {"status": "atualizado"}

    resultado = controller.alterar_configuracao_usuario(user_id=1, funcional=100, campo="ativo")

    assert resultado == {"status": "atualizado"}
    controller.usuario_service.alterar_configuracao_usuario.assert_called_once_with(100, "ativo")


@patch('src.contollers.controller_usuarios.service_validacao_estados')
def test_alterar_configuracao_erro_interno(mock_validador, controller):
    """Deve retornar status 500 se houver falha na alteração da configuração."""
    controller.usuario_service.alterar_configuracao_usuario.side_effect = Exception("Erro DB")

    with pytest.raises(HTTPException) as exc_info:
        controller.alterar_configuracao_usuario(user_id=1, funcional=100, campo="ativo")
    
    assert exc_info.value.status_code == 500


# ==============================================================================
# TESTES: ATUALIZAR USUÁRIO
# ==============================================================================

@patch('src.contollers.controller_usuarios.service_validacao_atualizacao_usuario')
def test_atualizar_usuario_com_senha(mock_validador, controller):
    """Deve atualizar os dados e gerar novo hash caso o campo senha esteja presente no payload."""
    mock_instancia = mock_validador.return_value
    mock_instancia.validar_atualizacoes.return_value = {"nome": "Novo Nome", "senha": "nova_senha"}
    controller.usuario_service.atualizar_usuario.return_value = {"status": "sucesso"}

    resultado = controller.atualizar_usuario(funcional=12345, payload={"nome": "Novo Nome", "senha": "nova_senha"})

    assert resultado == {"status": "sucesso"}
    # Verifica que o dicionário enviado para atualização trocou 'senha' por 'senha_hash'
    argumento_salvo = controller.usuario_service.atualizar_usuario.call_args[0][1]
    assert "senha_hash" in argumento_salvo
    assert "senha" not in argumento_salvo


@patch('src.contollers.controller_usuarios.service_validacao_atualizacao_usuario')
def test_atualizar_usuario_sem_senha(mock_validador, controller):
    """Deve atualizar apenas dados cadastrais comuns se a senha não for fornecida."""
    mock_instancia = mock_validador.return_value
    mock_instancia.validar_atualizacoes.return_value = {"nome": "Apenas Nome"}
    controller.usuario_service.atualizar_usuario.return_value = {"status": "sucesso"}

    resultado = controller.atualizar_usuario(funcional=12345, payload={"nome": "Apenas Nome"})

    assert resultado == {"status": "sucesso"}
    argumento_salvo = controller.usuario_service.atualizar_usuario.call_args[0][1]
    assert "senha_hash" not in argumento_salvo


@patch('src.contollers.controller_usuarios.service_validacao_atualizacao_usuario')
def test_atualizar_usuario_erro_interno(mock_validador, controller):
    """Deve retornar erro HTTP 500 se o service de banco falhar inesperadamente."""
    mock_instancia = mock_validador.return_value
    mock_instancia.validar_atualizacoes.return_value = {"nome": "Teste"}
    controller.usuario_service.atualizar_usuario.side_effect = Exception("Erro Conexão")

    with pytest.raises(HTTPException) as exc_info:
        controller.atualizar_usuario(funcional=12345, payload={})
    
    assert exc_info.value.status_code == 500