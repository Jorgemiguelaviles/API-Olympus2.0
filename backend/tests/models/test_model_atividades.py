# tests/models/test_model_atividades.py

from src.models.model_atividades import model_atividades


def test_model_atividades_criacao():

    atividade = model_atividades(
        codigo_atividade="123-uuid-teste",
        nome_atividade="RUN"
    )

    assert atividade.codigo_atividade == "123-uuid-teste"
    assert atividade.nome_atividade == "RUN"


def test_model_atividades_tablename():

    assert model_atividades.__tablename__ == "atividade"