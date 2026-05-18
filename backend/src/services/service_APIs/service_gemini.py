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

        Dados do usuário:

        {dados_formatados}

        Pedido do usuário:

        {prompt_usuario}
        """

        return prompt_completo


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

        return response.text

