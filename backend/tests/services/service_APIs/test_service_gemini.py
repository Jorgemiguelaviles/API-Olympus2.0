# tests/services/test_service_gemini.py

from unittest.mock import (
    MagicMock,
    patch
)

import pytest

from src.services.service_APIs.service_gemini import (
    service_gemini
)


# ==========================================
# FIXTURE
# ==========================================
@pytest.fixture
def service():

    with patch.dict(
        "os.environ",
        {
            "API_KEY_GEMINI": "fake-key"
        }
    ):

        with patch(
            "src.services.service_APIs.service_gemini.genai.Client"
        ):

            yield service_gemini()


# ==========================================
# INIT SUCESSO
# ==========================================
@patch(
    "src.services.service_APIs.service_gemini.genai.Client"
)
def test_init_success(
    mock_client
):

    with patch.dict(
        "os.environ",
        {
            "API_KEY_GEMINI": "fake-key"
        }
    ):

        service_gemini()

        mock_client.assert_called_once_with(
            api_key="fake-key"
        )


# ==========================================
# INIT SEM API KEY
# ==========================================
def test_init_sem_api_key():

    with patch.dict(
        "os.environ",
        {},
        clear=True
    ):

        with pytest.raises(ValueError) as erro:

            service_gemini()

        assert (
            str(erro.value)
            == "API_KEY_GEMINI não encontrada."
        )


# ==========================================
# SCHEMA PADRÃO
# ==========================================
def test_retorna_schema_resposta(
    service
):

    schema = (
        service.retorna_schema_resposta()
    )

    assert isinstance(
        schema,
        dict
    )

    assert "resumo" in schema

    assert "tendencias" in schema

    assert "conclusao" in schema


# ==========================================
# MONTA PROMPT
# ==========================================
def test_monta_prompt(
    service
):

    prompt = service.monta_prompt(
        dados_usuario=[
            "corrida",
            "natação"
        ],
        prompt_usuario=(
            "Analise evolução"
        )
    )

    assert (
        "corrida"
        in prompt
    )

    assert (
        "natação"
        in prompt
    )

    assert (
        "Analise evolução"
        in prompt
    )

    assert (
        "JSON válido"
        in prompt
    )


# ==========================================
# LIMPA RESPOSTA
# ==========================================
def test_limpa_resposta(
    service
):

    resposta = (
        "```json\n"
        '{"ok": true}'
        "\n```"
    )

    resultado = (
        service.limpa_resposta(
            resposta
        )
    )

    assert resultado == (
        '{"ok": true}'
    )


# ==========================================
# LIMPA RESPOSTA VAZIA
# ==========================================
def test_limpa_resposta_vazia(
    service
):

    with pytest.raises(ValueError) as erro:

        service.limpa_resposta("")

    assert (
        str(erro.value)
        == "Resposta vazia recebida da IA."
    )


# ==========================================
# VALIDA ESTRUTURA
# ==========================================
def test_valida_estrutura_resposta(
    service
):

    resposta = {
        "resumo": "ok"
    }

    resultado = (
        service
        .valida_estrutura_resposta(
            resposta
        )
    )

    assert (
        resultado["resumo"]
        == "ok"
    )

    assert (
        "tendencias"
        in resultado
    )

    assert (
        "conclusao"
        in resultado
    )


# ==========================================
# VALIDA ESTRUTURA INVÁLIDA
# ==========================================
def test_valida_estrutura_resposta_invalida(
    service
):

    with pytest.raises(ValueError) as erro:

        service.valida_estrutura_resposta(
            []
        )

    assert (
        str(erro.value)
        == "Resposta da IA não é um JSON válido."
    )


# ==========================================
# CONVERTE JSON SUCESSO
# ==========================================
def test_converte_resposta_json(
    service
):

    resposta = """
    {
        "resumo": "ok"
    }
    """

    resultado = (
        service.converte_resposta_json(
            resposta
        )
    )

    assert (
        resultado["resumo"]
        == "ok"
    )


# ==========================================
# CONVERTE JSON INVÁLIDO
# ==========================================
def test_converte_resposta_json_invalido(
    service
):

    with pytest.raises(ValueError) as erro:

        service.converte_resposta_json(
            "resposta inválida"
        )

    assert (
        str(erro.value)
        == "IA retornou JSON inválido."
    )


# ==========================================
# ANALISA DADOS SUCESSO
# ==========================================
def test_analisa_dados_sucesso():

    with patch.dict(
        "os.environ",
        {
            "API_KEY_GEMINI": "fake-key"
        }
    ):

        with patch(
            "src.services.service_APIs.service_gemini.genai.Client"
        ) as mock_client:

            response_mock = MagicMock()

            response_mock.text = """
            {
                "resumo": "Usuário evoluindo"
            }
            """

            client_instance = (
                MagicMock()
            )

            (
                client_instance
                .models
                .generate_content
                .return_value
            ) = response_mock

            mock_client.return_value = (
                client_instance
            )

            service = service_gemini()

            resultado = (
                service.analisa_dados(
                    dados_usuario=[
                        "corrida"
                    ],
                    prompt_usuario=(
                        "Analise"
                    )
                )
            )

            assert (
                resultado["resumo"]
                == "Usuário evoluindo"
            )


# ==========================================
# ANALISA DADOS SEM TEXT
# ==========================================
def test_analisa_dados_sem_text():

    with patch.dict(
        "os.environ",
        {
            "API_KEY_GEMINI": "fake-key"
        }
    ):

        with patch(
            "src.services.service_APIs.service_gemini.genai.Client"
        ) as mock_client:

            response_mock = MagicMock(
                spec=[]
            )

            client_instance = (
                MagicMock()
            )

            (
                client_instance
                .models
                .generate_content
                .return_value
            ) = response_mock

            mock_client.return_value = (
                client_instance
            )

            service = service_gemini()

            with pytest.raises(RuntimeError):

                service.analisa_dados(
                    dados_usuario=[],
                    prompt_usuario="teste"
                )


# ==========================================
# ANALISA DADOS RESPOSTA VAZIA
# ==========================================
def test_analisa_dados_resposta_vazia():

    with patch.dict(
        "os.environ",
        {
            "API_KEY_GEMINI": "fake-key"
        }
    ):

        with patch(
            "src.services.service_APIs.service_gemini.genai.Client"
        ) as mock_client:

            response_mock = MagicMock()

            response_mock.text = ""

            client_instance = (
                MagicMock()
            )

            (
                client_instance
                .models
                .generate_content
                .return_value
            ) = response_mock

            mock_client.return_value = (
                client_instance
            )

            service = service_gemini()

            with pytest.raises(RuntimeError):

                service.analisa_dados(
                    dados_usuario=[],
                    prompt_usuario="teste"
                )