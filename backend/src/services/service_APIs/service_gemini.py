import os
import json
import logging

from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ==========================================
# CONFIGURAÇÃO .ENV
# ==========================================
BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
    .parent
)

dotenv_path = BASE_DIR / ".env"

load_dotenv(dotenv_path)


logger = logging.getLogger(__name__)


class service_gemini:


    # ==========================================
    # CONSTRUTOR
    # ==========================================
    def __init__(self):

        chave_api = os.getenv(
            "API_KEY_GEMINI"
        )

        logger.info(
            "Carregando API Gemini."
        )

        logger.info(
            "Path .env: %s",
            dotenv_path
        )

        logger.info(
            "API encontrada: %s",
            bool(chave_api)
        )

        if not chave_api:

            raise ValueError(
                "API_KEY_GEMINI não encontrada."
            )

        self.client = genai.Client(
            api_key=chave_api
        )


    # ==========================================
    # SCHEMA PADRÃO
    # ==========================================
    @staticmethod
    def retorna_schema_resposta():

        return {

            "resumo": "",

            "tendencias": [],

            "sinais_fadiga": [],

            "recomendacoes_treino": [],

            "recomendacoes_recuperacao": [],

            "alertas": [],

            "conclusao": ""
        }


    # ==========================================
    # MONTA PROMPT
    # ==========================================
    def monta_prompt(
        self,
        dados_usuario: list,
        prompt_usuario: str
    ):

        dados_formatados = json.dumps(
            dados_usuario,
            indent=2,
            ensure_ascii=False
        )

        estrutura_json = json.dumps(
            self.retorna_schema_resposta(),
            indent=2,
            ensure_ascii=False
        )

        return f"""
Você é um especialista em análise de desempenho físico.

IMPORTANTE:
- Retorne SOMENTE JSON válido
- NÃO utilize markdown
- NÃO utilize comentários
- NÃO escreva texto fora do JSON

ESTRUTURA OBRIGATÓRIA:

{estrutura_json}

REGRAS:
- tendencias -> lista de strings
- sinais_fadiga -> lista de objetos
- recomendacoes_treino -> lista
- recomendacoes_recuperacao -> lista
- alertas -> lista
- conclusao -> string

Dados:

{dados_formatados}

Pedido:

{prompt_usuario}
"""


    # ==========================================
    # LIMPA RESPOSTA
    # ==========================================
    @staticmethod
    def limpa_resposta(
        resposta_texto: str
    ):

        if not resposta_texto:

            raise ValueError(
                "Resposta vazia recebida da IA."
            )

        return (
            resposta_texto
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    # ==========================================
    # VALIDA ESTRUTURA
    # ==========================================
    def valida_estrutura_resposta(
        self,
        resposta_json: dict
    ):

        if not isinstance(
            resposta_json,
            dict
        ):

            raise ValueError(
                "Resposta da IA não é um JSON válido."
            )

        estrutura = (
            self.retorna_schema_resposta()
        )

        for chave, valor in estrutura.items():

            if chave not in resposta_json:

                resposta_json[chave] = valor

        return resposta_json


    # ==========================================
    # CONVERTE RESPOSTA JSON
    # ==========================================
    def converte_resposta_json(
        self,
        resposta_texto: str
    ):

        try:

            resposta_limpa = (
                self.limpa_resposta(
                    resposta_texto
                )
            )

            resposta_json = json.loads(
                resposta_limpa
            )

            return self.valida_estrutura_resposta(
                resposta_json
            )

        except json.JSONDecodeError as erro:

            logger.error(
                "Erro ao converter JSON da IA: %s",
                str(erro)
            )

            raise ValueError(
                "IA retornou JSON inválido."
            )


    # ==========================================
    # GERA ANÁLISE
    # ==========================================
    def analisa_dados(
        self,
        dados_usuario: list,
        prompt_usuario: str
    ):

        logger.info(
            "Iniciando análise Gemini."
        )

        prompt = self.monta_prompt(
            dados_usuario,
            prompt_usuario
        )

        try:

            response = (
                self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
            )

            if not hasattr(
                response,
                "text"
            ):

                raise ValueError(
                    "Resposta Gemini sem atributo text."
                )

            if not response.text:

                raise ValueError(
                    "Gemini retornou resposta vazia."
                )

            resposta = (
                self.converte_resposta_json(
                    response.text
                )
            )

            logger.info(
                "Análise Gemini concluída com sucesso."
            )

            return resposta

        except Exception as erro:

            logger.exception(
                "Erro ao gerar análise Gemini."
            )

            raise RuntimeError(
                f"Erro ao gerar análise IA: {str(erro)}"
            )