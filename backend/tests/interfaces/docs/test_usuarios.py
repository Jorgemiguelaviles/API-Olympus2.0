# tests/interfaces/docs/test_docs_usuarios.py

from fastapi import status

from src.interfaces.docs.docs_usuarios import (
    DOC_CADASTRAR_USUARIO,
    DOC_LOGIN_USUARIO,
    DOC_LISTAR_USUARIOS,
    DOC_ALTERAR_CONFIGURACAO,
    DOC_ATUALIZAR_USUARIO
)

from src.interfaces.schemas.schema_usuarios import (
    UsuarioRespostaSchema,
    UsuarioListagemSchema
)


# ==========================================
# DOC CADASTRAR USUÁRIO
# ==========================================
def test_doc_cadastrar_usuario_response_model():

    assert (
        DOC_CADASTRAR_USUARIO["response_model"]
        == UsuarioRespostaSchema
    )


def test_doc_cadastrar_usuario_summary():

    assert (
        DOC_CADASTRAR_USUARIO["summary"]
        == "Cadastrar usuário"
    )


def test_doc_cadastrar_usuario_description():

    assert (
        DOC_CADASTRAR_USUARIO["description"]
        == "Cria um novo usuário no sistema."
    )


def test_doc_cadastrar_usuario_responses():

    responses = DOC_CADASTRAR_USUARIO["responses"]

    assert status.HTTP_201_CREATED in responses
    assert status.HTTP_400_BAD_REQUEST in responses
    assert status.HTTP_409_CONFLICT in responses


def test_doc_cadastrar_usuario_response_descriptions():

    responses = DOC_CADASTRAR_USUARIO["responses"]

    assert (
        responses[status.HTTP_201_CREATED]["description"]
        == "Usuário cadastrado com sucesso."
    )

    assert (
        responses[status.HTTP_400_BAD_REQUEST]["description"]
        == "Dados inválidos."
    )

    assert (
        responses[status.HTTP_409_CONFLICT]["description"]
        == "Usuário já existente."
    )


# ==========================================
# DOC LOGIN USUÁRIO
# ==========================================
def test_doc_login_usuario_summary():

    assert (
        DOC_LOGIN_USUARIO["summary"]
        == "Autenticar usuário"
    )


def test_doc_login_usuario_description():

    assert (
        DOC_LOGIN_USUARIO["description"]
        == "Realiza autenticação e retorna JWT."
    )


def test_doc_login_usuario_responses():

    responses = DOC_LOGIN_USUARIO["responses"]

    assert status.HTTP_200_OK in responses
    assert status.HTTP_401_UNAUTHORIZED in responses


def test_doc_login_usuario_response_descriptions():

    responses = DOC_LOGIN_USUARIO["responses"]

    assert (
        responses[status.HTTP_200_OK]["description"]
        == "Login realizado com sucesso."
    )

    assert (
        responses[status.HTTP_401_UNAUTHORIZED]["description"]
        == "Credenciais inválidas."
    )


# ==========================================
# DOC LISTAR USUÁRIOS
# ==========================================
def test_doc_listar_usuarios_response_model():

    assert (
        DOC_LISTAR_USUARIOS["response_model"]
        == list[UsuarioListagemSchema]
    )


def test_doc_listar_usuarios_summary():

    assert (
        DOC_LISTAR_USUARIOS["summary"]
        == "Listar usuários"
    )


def test_doc_listar_usuarios_description():

    assert (
        DOC_LISTAR_USUARIOS["description"]
        == "Retorna usuários paginados."
    )


# ==========================================
# DOC ALTERAR CONFIGURAÇÃO
# ==========================================
def test_doc_alterar_configuracao_summary():

    assert (
        DOC_ALTERAR_CONFIGURACAO["summary"]
        == "Alterar configuração do usuário"
    )


def test_doc_alterar_configuracao_description():

    assert (
        DOC_ALTERAR_CONFIGURACAO["description"]
        == "Altera permissões e status do usuário."
    )


# ==========================================
# DOC ATUALIZAR USUÁRIO
# ==========================================
def test_doc_atualizar_usuario_summary():

    assert (
        DOC_ATUALIZAR_USUARIO["summary"]
        == "Atualizar usuário"
    )


def test_doc_atualizar_usuario_description():

    assert (
        DOC_ATUALIZAR_USUARIO["description"]
        == "Atualiza dados do usuário."
    )