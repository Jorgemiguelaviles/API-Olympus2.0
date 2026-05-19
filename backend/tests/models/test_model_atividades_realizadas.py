# tests/models/test_model_atividades_realizadas.py

from datetime import datetime

from src.models.model_atividades_realizadas import (
    model_atividades_realizadas
)


def test_model_atividades_realizadas_criacao():

    data_teste = datetime.now()

    atividade_realizada = model_atividades_realizadas(
        id_atividade_realizada=1,
        funcional=1001,
        codigo_atividade="uuid-teste",
        descricao="Corrida de 5km",
        data_hora=data_teste
    )

    assert atividade_realizada.id_atividade_realizada == 1
    assert atividade_realizada.funcional == 1001
    assert atividade_realizada.codigo_atividade == "uuid-teste"
    assert atividade_realizada.descricao == "Corrida de 5km"
    assert atividade_realizada.data_hora == data_teste


def test_model_atividades_realizadas_tablename():

    assert (
        model_atividades_realizadas.__tablename__
        == "atividade_realizada"
    )