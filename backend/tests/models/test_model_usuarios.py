# tests/models/test_model_usuarios.py

from src.models.model_usuarios import model_usuarios


def test_model_usuarios_criacao():

    usuario = model_usuarios(
        funcional=1001,
        usuario="jorge",
        senha_hash="senha_hash_teste",
        nome="Jorge Miguel",
        usuario_root=True,
        usuario_ativado=True
    )

    assert usuario.funcional == 1001
    assert usuario.usuario == "jorge"
    assert usuario.senha_hash == "senha_hash_teste"
    assert usuario.nome == "Jorge Miguel"
    assert usuario.usuario_root is True
    assert usuario.usuario_ativado is True


def test_model_usuarios_tablename():

    assert model_usuarios.__tablename__ == "usuarios"