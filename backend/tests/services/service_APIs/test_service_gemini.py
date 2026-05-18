# tests/services/test_service_gemini.py

import pytest

from unittest.mock import Mock, patch

from src.services.service_APIs.service_gemini import (
    service_gemini
)


# ==========================================
# Teste construtor sem API KEY
# ==========================================
def test_init_sem_api_key():

    with pytest.raises(ValueError) as erro:

        service_gemini()

    assert (
        str(erro.value)
        == "API_KEY_GEMINI não encontrada no .env"
    )


# ==========================================
# Teste construtor com API KEY
# ==========================================
@patch(
    "src.services.service_APIs.service_gemini.genai.Client"
)
def test_init_com_api_key(
    mock_client
):

    service = service_gemini(
        chave_api="fake_key"
    )

    mock_client.assert_called_once_with(
        api_key="fake_key"
    )

    assert service.client == mock_client.return_value


# ==========================================
# Teste montagem do prompt
# ==========================================
@patch(
    "src.services.service_APIs.service_gemini.genai.Client"
)
def test_monta_prompt(
    mock_client
):

    service = service_gemini(
        chave_api="fake_key"
    )

    dados_usuario = [
        "Corrida de 5km",
        "Natação 30 minutos"
    ]

    prompt_usuario = (
        "Analise os dados físicos."
    )

    resultado = service.monta_prompt(
        dados_usuario=dados_usuario,
        prompt_usuario=prompt_usuario
    )

    assert (
        "Corrida de 5km"
        in resultado
    )

    assert (
        "Natação 30 minutos"
        in resultado
    )

    assert (
        "Analise os dados físicos."
        in resultado
    )

    assert (
        "especialista em análise de desempenho físico"
        in resultado
    )


# ==========================================
# Teste analisa_dados
# ==========================================
@patch(
    "src.services.service_APIs.service_gemini.genai.Client"
)
def test_analisa_dados(
    mock_client
):

    mock_response = Mock()

    mock_response.text = (
        "Usuário apresenta boa evolução."
    )

    mock_generate = Mock(
        return_value=mock_response
    )

    mock_models = Mock()

    mock_models.generate_content = (
        mock_generate
    )

    mock_client.return_value.models = (
        mock_models
    )

    service = service_gemini(
        chave_api="fake_key"
    )

    resultado = service.analisa_dados(
        dados_usuario=[
            "Corrida 5km"
        ],
        prompt_usuario=(
            "Analise a evolução."
        )
    )

    assert (
        resultado
        == "Usuário apresenta boa evolução."
    )

    mock_generate.assert_called_once()


# ==========================================
# Teste erro generate_content
# ==========================================
@patch(
    "src.services.service_APIs.service_gemini.genai.Client"
)
def test_analisa_dados_erro(
    mock_client
):

    mock_models = Mock()

    mock_models.generate_content.side_effect = (
        Exception("Erro Gemini")
    )

    mock_client.return_value.models = (
        mock_models
    )

    service = service_gemini(
        chave_api="fake_key"
    )

    with pytest.raises(Exception) as erro:

        service.analisa_dados(
            dados_usuario=[
                "Corrida"
            ],
            prompt_usuario=(
                "Analise."
            )
        )

    assert (
        str(erro.value)
        == "Erro Gemini"
    )