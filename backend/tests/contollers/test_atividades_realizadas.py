from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from src.contollers.controller_atividades_realizadas import (
    controller_atividades_realizadas
)


# ==========================================
# FIXTURE
# ==========================================
@pytest.fixture
def fake_db():
    return MagicMock()


@pytest.fixture
def controller(fake_db):

    with patch(
        "src.contollers.controller_atividades_realizadas.load_dotenv"
    ):

        with patch(
            "src.contollers.controller_atividades_realizadas.os.getenv",
            return_value="fake-key"
        ):

            return controller_atividades_realizadas(fake_db)


# ==========================================
# BUSCAR TODAS - SUCESSO
# ==========================================
def test_buscar_todas_atividades_sucesso(controller):

    atividade_mock = MagicMock()

    atividade_mock.funcional = 1
    atividade_mock.codigo_atividade = "abc"
    atividade_mock.descricao = "Natação"
    atividade_mock.data_hora = "2025-01-01"

    with patch(
        "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        mock_service.return_value.get_recupera_todas_atividades.return_value = [
            atividade_mock
        ]

        resultado = controller.buscar_todas_atividades()

        assert resultado[0]["funcional"] == 1
        assert resultado[0]["nome_atividade"] == "Natação"


# ==========================================
# BUSCAR TODAS - 404
# ==========================================
def test_buscar_todas_atividades_sem_resultado(controller):

    with patch(
        "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        mock_service.return_value.get_recupera_todas_atividades.return_value = []

        with pytest.raises(HTTPException) as erro:

            controller.buscar_todas_atividades()

        assert erro.value.status_code == 404


# ==========================================
# BUSCAR TODAS - EXCEPTION
# ==========================================
def test_buscar_todas_atividades_exception(controller):

    with patch(
        "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        mock_service.side_effect = Exception("erro fake")

        with pytest.raises(HTTPException) as erro:

            controller.buscar_todas_atividades()

        assert erro.value.status_code == 500


# ==========================================
# BUSCAR POR FUNCIONAL - SUCESSO
# ==========================================
def test_buscar_por_funcional_sucesso(controller):

    atividades_mock = [
        {
            "funcional": 1,
            "codigo_atividade": "abc",
            "descricao": "Musculação",
            "data_hora": "2025"
        }
    ]

    with patch(
        "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        mock_service.return_value.get_recupera_atividades_por_funcional.return_value = atividades_mock

        with patch.object(
            controller,
            "_gerar_analise_ia",
            return_value={"status": "ok"}
        ):

            resultado = controller.buscar_por_funcional(1)

            assert "atividades" in resultado
            assert "analise_ia" in resultado


# ==========================================
# BUSCAR POR FUNCIONAL - 404
# ==========================================
def test_buscar_por_funcional_404(controller):

    with patch(
        "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
    ) as mock_service:

        mock_service.return_value.get_recupera_atividades_por_funcional.return_value = []

        with pytest.raises(HTTPException) as erro:

            controller.buscar_por_funcional(1)

        assert erro.value.status_code == 404


# ==========================================
# GERAR ANALISE - SEM API KEY
# ==========================================
def test_gerar_analise_sem_api_key(fake_db):

    with patch(
        "src.contollers.controller_atividades_realizadas.os.getenv",
        return_value=None
    ):

        controller = controller_atividades_realizadas(fake_db)

        resultado = controller._gerar_analise_ia(
            ["Natação"],
            [{"nome_atividade": "Natação"}]
        )

        assert resultado["status"] == "no-api-key"


# ==========================================
# GERAR ANALISE - SUCESSO
# ==========================================
def test_gerar_analise_sucesso(controller):

    with patch(
        "src.contollers.controller_atividades_realizadas.service_gemini"
    ) as mock_gemini:

        mock_gemini.return_value.analisa_dados.return_value = {
            "analise": "Boa evolução"
        }

        resultado = controller._gerar_analise_ia(
            ["Natação"],
            [{"nome_atividade": "Natação"}]
        )

        assert resultado["status"] == "ok"
        assert resultado["analise"] == "Boa evolução"


# ==========================================
# GERAR ANALISE - FALLBACK
# ==========================================
def test_gerar_analise_fallback(controller):

    with patch(
        "src.contollers.controller_atividades_realizadas.service_gemini"
    ) as mock_gemini:

        mock_gemini.return_value.analisa_dados.side_effect = Exception(
            "gemini off"
        )

        resultado = controller._gerar_analise_ia(
            ["Natação"],
            [{"nome_atividade": "Natação"}]
        )

        assert resultado["status"] == "fallback"


# ==========================================
# CADASTRAR ATIVIDADE - SUCESSO
# ==========================================
def test_cadastrar_atividade_sucesso(controller):

    atividade_mock = MagicMock()

    atividade_mock.funcional = 1
    atividade_mock.codigo_atividade = "abc"
    atividade_mock.descricao = "Natação"
    atividade_mock.data_hora = "2025"

    with patch(
        "src.contollers.controller_atividades_realizadas.service_validacao_atividade"
    ):

        with patch(
            "src.contollers.controller_atividades_realizadas.service_atividades_realizadas"
        ) as mock_service:

            mock_service.return_value.salvar.return_value = atividade_mock

            resultado = controller.cadastrar_atividade({})

            assert resultado["status"] == "ok"
            assert resultado["atividade"]["nome_atividade"] == "Natação"


# ==========================================
# CADASTRAR ATIVIDADE - EXCEPTION
# ==========================================
def test_cadastrar_atividade_exception(controller):

    with patch(
        "src.contollers.controller_atividades_realizadas.service_validacao_atividade"
    ) as mock_validacao:

        mock_validacao.return_value.validar.side_effect = Exception(
            "erro fake"
        )

        with pytest.raises(HTTPException) as erro:

            controller.cadastrar_atividade({})

        assert erro.value.status_code == 500