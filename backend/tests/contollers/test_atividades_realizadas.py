from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from src.contollers.atividades_realizadas import (
    controller_atividades_realizadas
)


# ====================================================
# buscar_todas_atividades
# ====================================================

def test_buscar_todas_atividades_sucesso():

    fake_db = MagicMock()

    fake_response = [
        {"id": 1},
        {"id": 2}
    ]

    with patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        service = mock_service.return_value

        service.get_recupera_todas_atividades.return_value = (
            fake_response
        )

        controller = controller_atividades_realizadas(
            fake_db
        )

        result = controller.buscar_todas_atividades()

        assert result == fake_response


def test_buscar_todas_atividades_vazio():

    fake_db = MagicMock()

    with patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        service = mock_service.return_value

        service.get_recupera_todas_atividades.return_value = []

        controller = controller_atividades_realizadas(
            fake_db
        )

        try:

            controller.buscar_todas_atividades()

        except HTTPException as erro:

            assert erro.status_code == 404


def test_buscar_todas_atividades_erro():

    fake_db = MagicMock()

    with patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        service = mock_service.return_value

        service.get_recupera_todas_atividades.side_effect = (
            Exception("Erro banco")
        )

        controller = controller_atividades_realizadas(
            fake_db
        )

        try:

            controller.buscar_todas_atividades()

        except HTTPException as erro:

            assert erro.status_code == 500


# ====================================================
# buscar_por_funcional
# ====================================================

def test_buscar_por_funcional_sucesso():

    fake_db = MagicMock()

    fake_response = [
        {"funcional": 123456789}
    ]

    with patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        service = mock_service.return_value

        service.get_recupera_atividades_por_funcional.return_value = (
            fake_response
        )

        controller = controller_atividades_realizadas(
            fake_db
        )

        result = controller.buscar_por_funcional(
            123456789
        )

        assert result == fake_response


def test_buscar_por_funcional_vazio():

    fake_db = MagicMock()

    with patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        service = mock_service.return_value

        service.get_recupera_atividades_por_funcional.return_value = []

        controller = controller_atividades_realizadas(
            fake_db
        )

        try:

            controller.buscar_por_funcional(
                123456789
            )

        except HTTPException as erro:

            assert erro.status_code == 404


def test_buscar_por_funcional_erro():

    fake_db = MagicMock()

    with patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        service = mock_service.return_value

        service.get_recupera_atividades_por_funcional.side_effect = (
            Exception("Erro banco")
        )

        controller = controller_atividades_realizadas(
            fake_db
        )

        try:

            controller.buscar_por_funcional(
                123456789
            )

        except HTTPException as erro:

            assert erro.status_code == 500


# ====================================================
# cadastrar_atividade
# ====================================================

def test_cadastrar_atividade_sucesso():

    fake_db = MagicMock()

    payload = {
        "funcional": 123456789,
        "codigo_atividade": 1
    }

    with patch(
        "src.contollers.atividades_realizadas.service_validacao_atividade"
    ) as mock_validacao, patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        mock_validacao.return_value.validar.return_value = None

        mock_service.return_value.salvar.return_value = (
            payload
        )

        controller = controller_atividades_realizadas(
            fake_db
        )

        result = controller.cadastrar_atividade(
            payload
        )

        assert result == payload


def test_cadastrar_atividade_erro_validacao():

    fake_db = MagicMock()

    payload = {
        "funcional": 123456789
    }

    with patch(
        "src.contollers.atividades_realizadas.service_validacao_atividade"
    ) as mock_validacao:

        mock_validacao.return_value.validar.side_effect = (
            HTTPException(
                status_code=400,
                detail="Erro validação"
            )
        )

        controller = controller_atividades_realizadas(
            fake_db
        )

        try:

            controller.cadastrar_atividade(
                payload
            )

        except HTTPException as erro:

            assert erro.status_code == 400


def test_cadastrar_atividade_erro_interno():

    fake_db = MagicMock()

    payload = {
        "funcional": 123456789
    }

    with patch(
        "src.contollers.atividades_realizadas.service_validacao_atividade"
    ) as mock_validacao, patch(
        "src.contollers.atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        mock_validacao.return_value.validar.return_value = None

        mock_service.return_value.salvar.side_effect = (
            Exception("Erro persistência")
        )

        controller = controller_atividades_realizadas(
            fake_db
        )

        try:

            controller.cadastrar_atividade(
                payload
            )

        except HTTPException as erro:

            assert erro.status_code == 500