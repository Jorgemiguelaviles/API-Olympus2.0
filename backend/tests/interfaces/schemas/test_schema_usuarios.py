# tests/interfaces/test_schema_usuarios.py

import pytest
from pydantic import ValidationError

from src.interfaces.schemas.schema_usuarios import (
    UsuarioCriacaoSchema,
    UsuarioLoginSchema,
    UsuarioRespostaSchema,
    UsuarioListagemSchema,
    UsuarioConfiguracaoSchema,
    UsuarioAtualizacaoSchema
)


# ==========================================
# USUARIO CRIACAO
# ==========================================
def test_usuario_criacao_schema_success():

    schema = UsuarioCriacaoSchema(
        usuario="jorge@gmail.com",
        senha="Vava@0909",
        nome="Jorge Miguel"
    )

    assert schema.usuario == "jorge@gmail.com"
    assert schema.senha == "Vava@0909"
    assert schema.nome == "Jorge Miguel"


def test_usuario_criacao_schema_invalid_email():

    with pytest.raises(ValidationError):

        UsuarioCriacaoSchema(
            usuario="email_invalido",
            senha="123456",
            nome="Jorge"
        )


def test_usuario_criacao_schema_short_password():

    with pytest.raises(ValidationError):

        UsuarioCriacaoSchema(
            usuario="jorge@gmail.com",
            senha="123",
            nome="Jorge"
        )


def test_usuario_criacao_schema_short_name():

    with pytest.raises(ValidationError):

        UsuarioCriacaoSchema(
            usuario="jorge@gmail.com",
            senha="123456",
            nome="Jo"
        )


def test_usuario_criacao_schema_example():

    schema = UsuarioCriacaoSchema.model_json_schema()

    example = schema["example"]

    assert example["usuario"] == "jorge@gmail.com"
    assert example["senha"] == "Vava@0909"
    assert example["nome"] == "Jorge Miguel"


# ==========================================
# LOGIN
# ==========================================
def test_usuario_login_schema_success():

    schema = UsuarioLoginSchema(
        usuario="jorge@gmail.com",
        senha="123456"
    )

    assert schema.usuario == "jorge@gmail.com"
    assert schema.senha == "123456"


def test_usuario_login_schema_invalid_email():

    with pytest.raises(ValidationError):

        UsuarioLoginSchema(
            usuario="invalido",
            senha="123456"
        )


def test_usuario_login_schema_missing_password():

    with pytest.raises(ValidationError):

        UsuarioLoginSchema(
            usuario="jorge@gmail.com"
        )


def test_usuario_login_schema_example():

    schema = UsuarioLoginSchema.model_json_schema()

    example = schema["example"]

    assert example["usuario"] == "jorge@gmail.com"
    assert example["senha"] == "123456"


# ==========================================
# USUARIO RESPOSTA
# ==========================================
def test_usuario_resposta_schema_success():

    schema = UsuarioRespostaSchema(
        funcional=1,
        usuario="jorge@gmail.com",
        nome="Jorge Miguel",
        usuario_root=True,
        usuario_ativado=True
    )

    assert schema.funcional == 1
    assert schema.usuario_root is True
    assert schema.usuario_ativado is True


def test_usuario_resposta_schema_missing_fields():

    with pytest.raises(ValidationError):

        UsuarioRespostaSchema(
            funcional=1
        )


# ==========================================
# USUARIO LISTAGEM
# ==========================================
def test_usuario_listagem_schema_success():

    schema = UsuarioListagemSchema(
        funcional=10,
        usuario="jorge@gmail.com",
        nome="Jorge Miguel",
        usuario_root=False,
        usuario_ativado=True
    )

    assert schema.funcional == 10
    assert schema.usuario == "jorge@gmail.com"


# ==========================================
# CONFIGURACAO
# ==========================================
def test_usuario_configuracao_schema_success():

    schema = UsuarioConfiguracaoSchema(
        funcional=100,
        campo="usuario_root"
    )

    assert schema.funcional == 100
    assert schema.campo == "usuario_root"


def test_usuario_configuracao_schema_invalid_literal():

    with pytest.raises(ValidationError):

        UsuarioConfiguracaoSchema(
            funcional=100,
            campo="campo_invalido"
        )


def test_usuario_configuracao_schema_example():

    schema = UsuarioConfiguracaoSchema.model_json_schema()

    example = schema["example"]

    assert example["funcional"] == 100000000
    assert example["campo"] == "usuario_root"


# ==========================================
# ATUALIZACAO
# ==========================================
def test_usuario_atualizacao_schema_success():

    schema = UsuarioAtualizacaoSchema(
        funcional=1,
        nome="Novo Nome",
        usuario="novo@gmail.com",
        senha="novaSenha123"
    )

    assert schema.funcional == 1
    assert schema.nome == "Novo Nome"
    assert schema.usuario == "novo@gmail.com"


def test_usuario_atualizacao_schema_only_funcional():

    schema = UsuarioAtualizacaoSchema(
        funcional=1
    )

    assert schema.funcional == 1
    assert schema.nome is None
    assert schema.usuario is None
    assert schema.senha is None


def test_usuario_atualizacao_schema_invalid_email():

    with pytest.raises(ValidationError):

        UsuarioAtualizacaoSchema(
            funcional=1,
            usuario="email_invalido"
        )


def test_usuario_atualizacao_schema_example():

    schema = UsuarioAtualizacaoSchema.model_json_schema()

    example = schema["example"]

    assert example["funcional"] == 100000000
    assert example["nome"] == "Jorge Miguel"
    assert example["usuario"] == "jorge@gmail.com"
    assert example["senha"] == "novaSenha123"