from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from src.contollers.atividades_existentes import (
    controller_atividade_existente
)


# ==========================================
# Fluxo de sucesso
# ==========================================
def test_gerencia_atividades_sucesso():

    fake_db = MagicMock()

    fake_response = [
        {
            "codigo_atividade": 1,
            "nome_atividade": "Corrida"
        },
        {
            "codigo_atividade": 2,
            "nome_atividade": "Musculação"
        }
    ]

    with patch(
        "src.contollers.atividades_existentes.service_atividades"
    ) as mock_service:

        service_instance = mock_service.return_value

        service_instance.buscar_todas_atividades.return_value = (
            fake_response
        )

        controller = controller_atividade_existente(
            fake_db
        )

        result = controller.gerencia_atividades()

        assert result == fake_response


# ==========================================
# Lista vazia → 404
# ==========================================
def test_gerencia_atividades_sem_resultados():

    fake_db = MagicMock()

    with patch(
        "src.contollers.atividades_existentes.service_atividades"
    ) as mock_service:

        service_instance = mock_service.return_value

        service_instance.buscar_todas_atividades.return_value = []

        controller = controller_atividade_existente(
            fake_db
        )

        try:

            controller.gerencia_atividades()

        except HTTPException as erro:

            assert erro.status_code == 404
            assert erro.detail == (
                "Nenhuma atividade encontrada."
            )


# ==========================================
# HTTPException deve ser propagada
# ==========================================
def test_gerencia_atividades_http_exception():

    fake_db = MagicMock()

    with patch(
        "src.contollers.atividades_existentes.service_atividades"
    ) as mock_service:

        service_instance = mock_service.return_value

        service_instance.buscar_todas_atividades.side_effect = (
            HTTPException(
                status_code=401,
                detail="Não autorizado"
            )
        )

        controller = controller_atividade_existente(
            fake_db
        )

        try:

            controller.gerencia_atividades()

        except HTTPException as erro:

            assert erro.status_code == 401
            assert erro.detail == (
                "Não autorizado"
            )


# ==========================================
# Exception genérica → 500
# ==========================================
def test_gerencia_atividades_erro_interno():

    fake_db = MagicMock()

    with patch(
        "src.contollers.atividades_existentes.service_atividades"
    ) as mock_service:

        service_instance = mock_service.return_value

        service_instance.buscar_todas_atividades.side_effect = (
            Exception("Erro banco")
        )

        controller = controller_atividade_existente(
            fake_db
        )

        try:

            controller.gerencia_atividades()

        except HTTPException as erro:

            assert erro.status_code == 500
            assert (
                "Erro interno ao consultar atividades"
                in erro.detail
            )