# tests/controllers/test_controller_atividades_realizadas.py

from datetime import datetime
from unittest.mock import (
    MagicMock,
    patch
)

import pytest
from fastapi import HTTPException

from src.contollers.controller_atividades_realizadas import (
    controller_atividades_realizadas
)


# ==========================================
# FIXTURE
# ==========================================
@pytest.fixture
def db_mock():

    return MagicMock()


# ==========================================
# INIT
# ==========================================
def test_init_controller(
    db_mock
):

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    assert controller.db == db_mock


# ==========================================
# SERIALIZA DICT
# ==========================================
def test_serializa_atividade_dict():

    atividade = {

        "funcional": 1,

        "codigo_atividade":
        "SUPINO-001",

        "descricao":
        "Supino reto",

        "data_hora":
        datetime.now()
    }

    resultado = (
        controller_atividades_realizadas
        .serializa_atividade(
            atividade
        )
    )

    assert resultado["funcional"] == 1

    assert (
        resultado["codigo_atividade"]
        == "SUPINO-001"
    )

    assert (
        resultado["nome_atividade"]
        == "Supino reto"
    )


# ==========================================
# SERIALIZA OBJETO
# ==========================================
def test_serializa_atividade_objeto():

    atividade = MagicMock()

    atividade.funcional = 1

    atividade.codigo_atividade = (
        "SUPINO-001"
    )

    atividade.descricao = (
        "Supino reto"
    )

    atividade.data_hora = (
        datetime.now()
    )

    resultado = (
        controller_atividades_realizadas
        .serializa_atividade(
            atividade
        )
    )

    assert resultado["funcional"] == 1

    assert (
        resultado["codigo_atividade"]
        == "SUPINO-001"
    )

    assert (
        resultado["nome_atividade"]
        == "Supino reto"
    )


# ==========================================
# BUSCAR TODAS - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_todas_sucesso(
    mock_service,
    db_mock
):

    atividade = {

        "funcional": 1,

        "codigo_atividade":
        "SUPINO-001",

        "descricao":
        "Supino reto",

        "data_hora":
        datetime.now()
    }

    service_instance = (
        MagicMock()
    )

    service_instance.get_recupera_todas_atividades.return_value = [
        atividade
    ]

    mock_service.return_value = (
        service_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    resultado = (
        controller
        .buscar_todas_atividades()
    )

    assert len(resultado) == 1

    assert (
        resultado[0]["codigo_atividade"]
        == "SUPINO-001"
    )


# ==========================================
# BUSCAR TODAS - 404
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_todas_not_found(
    mock_service,
    db_mock
):

    service_instance = (
        MagicMock()
    )

    service_instance.get_recupera_todas_atividades.return_value = []

    mock_service.return_value = (
        service_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        controller.buscar_todas_atividades()

    assert (
        erro.value.status_code
        == 404
    )


# ==========================================
# BUSCAR TODAS - ERRO INTERNO
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_todas_erro(
    mock_service,
    db_mock
):

    service_instance = (
        MagicMock()
    )

    service_instance.get_recupera_todas_atividades.side_effect = (
        Exception("Erro banco")
    )

    mock_service.return_value = (
        service_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        controller.buscar_todas_atividades()

    assert (
        erro.value.status_code
        == 500
    )


# ==========================================
# BUSCAR POR FUNCIONAL - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.gerar_analise_ia_task"
)
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_por_funcional_sucesso(
    mock_service,
    mock_task,
    db_mock
):

    atividade = {

        "funcional": 1,

        "codigo_atividade":
        "SUPINO-001",

        "descricao":
        "Supino reto",

        "data_hora":
        datetime.now()
    }

    service_instance = (
        MagicMock()
    )

    service_instance.get_recupera_atividades_por_funcional.return_value = [
        atividade
    ]

    mock_service.return_value = (
        service_instance
    )

    task_mock = MagicMock()

    task_mock.id = "abc123"

    mock_task.delay.return_value = (
        task_mock
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    resultado = (
        controller.buscar_por_funcional(
            1
        )
    )

    assert (
        resultado["analise_ia"]["task_id"]
        == "abc123"
    )

    assert (
        resultado["analise_ia"]["status"]
        == "processando"
    )


# ==========================================
# BUSCAR POR FUNCIONAL - 404
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_por_funcional_not_found(
    mock_service,
    db_mock
):

    service_instance = (
        MagicMock()
    )

    service_instance.get_recupera_atividades_por_funcional.return_value = []

    mock_service.return_value = (
        service_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        controller.buscar_por_funcional(
            1
        )

    assert (
        erro.value.status_code
        == 404
    )


# ==========================================
# BUSCAR POR FUNCIONAL - ERRO
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_buscar_por_funcional_erro(
    mock_service,
    db_mock
):

    service_instance = (
        MagicMock()
    )

    service_instance.get_recupera_atividades_por_funcional.side_effect = (
        Exception("Erro banco")
    )

    mock_service.return_value = (
        service_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        controller.buscar_por_funcional(
            1
        )

    assert (
        erro.value.status_code
        == 500
    )


# ==========================================
# CADASTRAR - SUCESSO
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_validacao_atividade"
)
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_cadastrar_sucesso(
    mock_service,
    mock_validacao,
    db_mock
):

    atividade = {

        "funcional": 1,

        "codigo_atividade":
        "SUPINO-001",

        "descricao":
        "Supino reto",

        "data_hora":
        datetime.now()
    }

    service_instance = (
        MagicMock()
    )

    service_instance.salvar.return_value = (
        atividade
    )

    mock_service.return_value = (
        service_instance
    )

    validacao_instance = (
        MagicMock()
    )

    mock_validacao.return_value = (
        validacao_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    payload = {
        "descricao":
        "Supino reto"
    }

    resultado = (
        controller.cadastrar_atividade(
            payload
        )
    )

    assert (
        resultado["status"]
        == "ok"
    )

    validacao_instance.validar.assert_called_once()


# ==========================================
# CADASTRAR - HTTP ERROR
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_validacao_atividade"
)
def test_cadastrar_http_error(
    mock_validacao,
    db_mock
):

    validacao_instance = (
        MagicMock()
    )

    validacao_instance.validar.side_effect = (
        HTTPException(
            status_code=400,
            detail="Erro validação"
        )
    )

    mock_validacao.return_value = (
        validacao_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        controller.cadastrar_atividade(
            {}
        )

    assert (
        erro.value.status_code
        == 400
    )


# ==========================================
# CADASTRAR - ERRO INTERNO
# ==========================================
@patch(
    "src.contollers.controller_atividades_realizadas.service_validacao_atividade"
)
@patch(
    "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
)
def test_cadastrar_erro(
    mock_service,
    mock_validacao,
    db_mock
):

    validacao_instance = (
        MagicMock()
    )

    mock_validacao.return_value = (
        validacao_instance
    )

    service_instance = (
        MagicMock()
    )

    service_instance.salvar.side_effect = (
        Exception("Erro salvar")
    )

    mock_service.return_value = (
        service_instance
    )

    controller = (
        controller_atividades_realizadas(
            db_mock
        )
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        controller.cadastrar_atividade(
            {}
        )

    assert (
        erro.value.status_code
        == 500
    )