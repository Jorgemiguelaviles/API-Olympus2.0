from google import genai
import json


class service_gemini:

    # ==========================================
    # Construtor
    # ==========================================
    def __init__(self, chave_api=None):

        if not chave_api:

            raise ValueError(
                "API_KEY_GEMINI não encontrada no .env"
            )

        self.client = genai.Client(
            api_key=chave_api
        )

    # ==========================================
    # Schema padrão da resposta
    # ==========================================
    def retorna_schema_resposta(self):

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
    # Montar prompt
    # ==========================================
    def monta_prompt(
        self,
        dados_usuario: list,
        prompt_usuario: str,
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

        prompt_completo = f"""
Você é um especialista em análise de desempenho físico.

Analise os dados abaixo e gere:

1. Tendência das próximas semanas
2. Possíveis sinais de fadiga
3. Recomendações de treino
4. Recomendações de recuperação

OBS:
- Fique atento a possíveis sinais de overtraining.
- Analise quedas de desempenho.
- Analise frequência cardíaca elevada.
- Analise distúrbios do sono.
- Analise mudanças de humor.
- Caso encontre sinais de excesso, recomende redução de intensidade.

IMPORTANTE:
Caso existam poucos dados, considere que o usuário está no início da jornada fitness.

Mesmo com poucos dados:
- Gere uma análise coerente.
- Sugira melhorias produtivas.
- Oriente evolução gradual.
- Evite respostas genéricas.

IMPORTANTE:
- Retorne SOMENTE um JSON válido.
- NÃO utilize markdown.
- NÃO utilize ```json.
- NÃO escreva nenhum texto fora do JSON.
- NÃO utilize comentários.

ESTRUTURA OBRIGATÓRIA:

{estrutura_json}

REGRAS IMPORTANTES:
- "tendencias" deve ser uma lista de strings.
- "sinais_fadiga" deve ser uma lista de objetos contendo:
    {{
        "nivel": "baixo/médio/alto",
        "descricao": "texto"
    }}

- "recomendacoes_treino" deve ser uma lista.
- "recomendacoes_recuperacao" deve ser uma lista.
- "alertas" deve ser uma lista.
- "conclusao" deve ser uma string.

Dados do usuário:

{dados_formatados}

Pedido do usuário:

{prompt_usuario}
"""

        return prompt_completo

    # ==========================================
    # Limpar resposta da IA
    # ==========================================
    def limpa_resposta(
        self,
        resposta_texto: str
    ):

        resposta_limpa = (
            resposta_texto
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return resposta_limpa

    # ==========================================
    # Validar estrutura da resposta
    # ==========================================
    def valida_estrutura_resposta(
        self,
        resposta_json: dict
    ):

        estrutura_padrao = self.retorna_schema_resposta()

        for chave in estrutura_padrao.keys():

            if chave not in resposta_json:

                resposta_json[chave] = estrutura_padrao[chave]

        return resposta_json

    # ==========================================
    # Formatar resposta final
    # ==========================================
    def formata_resposta(
        self,
        resposta_texto: str
    ):

        try:

            resposta_limpa = self.limpa_resposta(
                resposta_texto
            )

            resposta_json = json.loads(
                resposta_limpa
            )

            resposta_json = self.valida_estrutura_resposta(
                resposta_json
            )

            return {
                "sucesso": True,
                "dados": resposta_json
            }

        except Exception as erro:

            return {
                "sucesso": False,
                "erro": str(erro),
                "resposta_original": resposta_texto
            }

    # ==========================================
    # Gerar análise IA
    # ==========================================
    def analisa_dados(
        self,
        dados_usuario: list,
        prompt_usuario: str
    ):

        print(
            "Realizando análise com Gemini..."
        )

        prompt = self.monta_prompt(
            dados_usuario,
            prompt_usuario
        )

        try:

            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            )

            resposta_formatada = self.formata_resposta(
                response.text
            )

            return resposta_formatada

        except Exception as erro:

            return {
                "sucesso": False,
                "erro": f"Erro ao gerar análise: {str(erro)}"
            }