# tests/infraestructure/tasks/test_task_analise_ia.py

from unittest.mock import (
    MagicMock,
    patch
)

from src.infraestructure.tasks.task_analise_ia import (
    gerar_analise_ia_task
)


# ==========================================
# TASK - SUCESSO
# ==========================================
@patch(
    "src.infraestructure.tasks.task_analise_ia.service_gemini"
)
def test_gerar_analise_ia_task_sucesso(
    mock_service_gemini
):

    atividades = [

        {
            "nome_atividade":
            "SUPINO RETO"
        },

        {
            "nome_atividade":
            "AGACHAMENTO"
        }
    ]

    resultado_mock = {

        "resumo":
        "Boa evolução",

        "tendencias": [
            "Aumento de carga"
        ]
    }

    service_instance = (
        MagicMock()
    )

    service_instance.analisa_dados.return_value = (
        resultado_mock
    )

    mock_service_gemini.return_value = (
        service_instance
    )

    resultado = (
        gerar_analise_ia_task(
            atividades
        )
    )

    assert resultado == resultado_mock

    service_instance.analisa_dados.assert_called_once_with(

        dados_usuario=[
            "SUPINO RETO",
            "AGACHAMENTO"
        ],

        prompt_usuario=(
            "Analise a evolução física."
        )
    )


# ==========================================
# TASK - IGNORA NOME VAZIO
# ==========================================
@patch(
    "src.infraestructure.tasks.task_analise_ia.service_gemini"
)
def test_gerar_analise_ia_task_ignora_vazios(
    mock_service_gemini
):

    atividades = [

        {
            "nome_atividade":
            "SUPINO"
        },

        {
            "nome_atividade":
            None
        },

        {}
    ]

    service_instance = (
        MagicMock()
    )

    service_instance.analisa_dados.return_value = (
        {"ok": True}
    )

    mock_service_gemini.return_value = (
        service_instance
    )

    gerar_analise_ia_task(
        atividades
    )

    service_instance.analisa_dados.assert_called_once_with(

        dados_usuario=[
            "SUPINO"
        ],

        prompt_usuario=(
            "Analise a evolução física."
        )
    )


# ==========================================
# TASK - LISTA VAZIA
# ==========================================
@patch(
    "src.infraestructure.tasks.task_analise_ia.service_gemini"
)
def test_gerar_analise_ia_task_lista_vazia(
    mock_service_gemini
):

    service_instance = (
        MagicMock()
    )

    service_instance.analisa_dados.return_value = (
        {"ok": True}
    )

    mock_service_gemini.return_value = (
        service_instance
    )

    resultado = (
        gerar_analise_ia_task([])
    )

    assert resultado == {
        "ok": True
    }

    service_instance.analisa_dados.assert_called_once_with(

        dados_usuario=[],

        prompt_usuario=(
            "Analise a evolução física."
        )
    )


# ==========================================
# TASK - ERRO GEMINI
# ==========================================
@patch(
    "src.infraestructure.tasks.task_analise_ia.service_gemini"
)
def test_gerar_analise_ia_task_erro(
    mock_service_gemini
):

    atividades = [

        {
            "nome_atividade":
            "SUPINO"
        }
    ]

    service_instance = (
        MagicMock()
    )

    service_instance.analisa_dados.side_effect = (
        Exception("Erro IA")
    )

    mock_service_gemini.return_value = (
        service_instance
    )

    try:

        gerar_analise_ia_task(
            atividades
        )

        assert False

    except Exception as erro:

        assert str(erro) == (
            "Erro IA"
        )
