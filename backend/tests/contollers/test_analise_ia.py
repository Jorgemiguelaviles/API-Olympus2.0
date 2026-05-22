import pytest

from fastapi import HTTPException

from src.contollers.controller_analise_ia import (
    controller_analise_ia
)


# ==========================================
# MOCK TASK
# ==========================================
class MockTask:


    def __init__(
        self,
        state,
        result=None
    ):

        self.state = state
        self.result = result


# ==========================================
# TESTE - STATUS PENDING
# ==========================================
def test_busca_status_pending(
    monkeypatch
):

    def mock_async_result(
        task_id,
        app=None
    ):

        return MockTask(
            state="PENDING"
        )

    monkeypatch.setattr(
        "src.contollers.controller_analise_ia.AsyncResult",
        mock_async_result
    )

    controller = (
        controller_analise_ia()
    )

    response = (
        controller
        .buscar_status_analise(
            "123"
        )
    )

    assert response == {

        "status":
        "processando",

        "resultado":
        None,

        "erro":
        None
    }


# ==========================================
# TESTE - STATUS SUCCESS
# ==========================================
def test_busca_status_success(
    monkeypatch
):

    resultado_mock = {
        "analise": "ok"
    }

    def mock_async_result(
        task_id,
        app=None
    ):

        return MockTask(
            state="SUCCESS",
            result=resultado_mock
        )

    monkeypatch.setattr(
        "src.contollers.controller_analise_ia.AsyncResult",
        mock_async_result
    )

    controller = (
        controller_analise_ia()
    )

    response = (
        controller
        .buscar_status_analise(
            "123"
        )
    )

    assert response == {

        "status":
        "concluido",

        "resultado":
        resultado_mock,

        "erro":
        None
    }


# ==========================================
# TESTE - STATUS FAILURE
# ==========================================
def test_busca_status_failure(
    monkeypatch
):

    def mock_async_result(
        task_id,
        app=None
    ):

        return MockTask(
            state="FAILURE",
            result="Erro interno"
        )

    monkeypatch.setattr(
        "src.contollers.controller_analise_ia.AsyncResult",
        mock_async_result
    )

    controller = (
        controller_analise_ia()
    )

    response = (
        controller
        .buscar_status_analise(
            "123"
        )
    )

    assert response == {

        "status":
        "erro",

        "resultado":
        None,

        "erro":
        "Erro interno"
    }


# ==========================================
# TESTE - OUTRO STATUS
# ==========================================
def test_busca_status_custom(
    monkeypatch
):

    def mock_async_result(
        task_id,
        app=None
    ):

        return MockTask(
            state="RETRY"
        )

    monkeypatch.setattr(
        "src.contollers.controller_analise_ia.AsyncResult",
        mock_async_result
    )

    controller = (
        controller_analise_ia()
    )

    response = (
        controller
        .buscar_status_analise(
            "123"
        )
    )

    assert response == {

        "status":
        "RETRY",

        "resultado":
        None,

        "erro":
        None
    }


# ==========================================
# TESTE - EXCEPTION
# ==========================================
def test_busca_status_exception(
    monkeypatch
):

    def mock_async_result(
        task_id,
        app=None
    ):

        raise Exception(
            "Erro inesperado"
        )

    monkeypatch.setattr(
        "src.contollers.controller_analise_ia.AsyncResult",
        mock_async_result
    )

    controller = (
        controller_analise_ia()
    )

    with pytest.raises(
        HTTPException
    ) as erro:

        controller.buscar_status_analise(
            "123"
        )

    assert (
        erro.value.status_code
        == 500
    )

    assert (
        erro.value.detail
        == "Erro inesperado"
    )