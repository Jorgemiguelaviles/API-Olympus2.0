import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import HTTPException

from src.services.service_APIs.service_gemini import service_gemini
from src.services.validadores.valida_atividades_realizadas import service_validacao_atividade
from src.services.service_bancos.atividades_realizadas import (
    service_atividades_realizadas
)


class controller_atividades_realizadas:

    def __init__(self, db):
        self.db = db

        # 🔥 ENV carregado uma única vez
        BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
        load_dotenv(dotenv_path=BASE_DIR / ".env")

        self.chave_api = os.getenv("API_KEY_GEMINI")


    # ==========================================
    # BUSCAR TODAS
    # ==========================================
    def buscar_todas_atividades(self):

        try:
            service = service_atividades_realizadas(self.db)
            atividades = service.get_recupera_todas_atividades()

            if not atividades:
                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma atividade encontrada."
                )

            # 🔥 NORMALIZAÇÃO (IMPORTANTE PRO SCHEMA)
            return [
                {
                    "funcional": a.funcional,
                    "codigo_atividade": a.codigo_atividade,
                    "nome_atividade": a.descricao,  # 👈 compatível com schema
                    "data_hora": a.data_hora
                }
                for a in atividades
            ]

        except HTTPException:
            raise

        except Exception as erro:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao consultar atividades: {str(erro)}"
            )


    # ==========================================
    # BUSCAR POR FUNCIONAL
    # ==========================================
    def buscar_por_funcional(self, funcional: int):

        try:
            service = service_atividades_realizadas(self.db)
            atividades = service.get_recupera_atividades_por_funcional(funcional)

            if not atividades:
                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma atividade encontrada para este funcional."
                )

            # 🔥 normalização (IMPORTANTE)
            atividades_formatadas = [
                {
                    "funcional": a["funcional"],
                    "codigo_atividade": a["codigo_atividade"],
                    "nome_atividade": a.get("descricao"),
                    "data_hora": a["data_hora"]
                }
                for a in atividades
            ]

            descricoes = [
                a["nome_atividade"]
                for a in atividades_formatadas
                if a.get("nome_atividade")
            ]

            analise_ia = self._gerar_analise_ia(
                descricoes,
                atividades_formatadas
            )

            return {
                "atividades": atividades_formatadas,
                "analise_ia": analise_ia
            }

        except HTTPException:
            raise

        except Exception as erro:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao consultar funcional: {str(erro)}"
            )


    # ==========================================
    # IA ISOLADA (SEGURO + CONSISTENTE)
    # ==========================================
    def _gerar_analise_ia(self, descricoes, atividades):

        if not self.chave_api:
            return {
                "status": "no-api-key",
                "mensagem": "API_KEY_GEMINI não configurada",
                "resumo": {
                    "total_treinos": len(atividades),
                    "ultima_atividade": atividades[-1]["nome_atividade"] if atividades else None
                },
                "analise": None
            }

        try:
            resultado = service_gemini(self.chave_api).analisa_dados(
                dados_usuario=descricoes,
                prompt_usuario=(
                    "Analise a evolução física do usuário "
                    "com base nos treinos realizados."
                )
            )

            # 🔥 CORREÇÃO PRINCIPAL AQUI
            if not isinstance(resultado, dict):
                resultado = {
                    "sucesso": False,
                    "erro": "Resposta inválida da IA"
                }

            return {
                "status": "ok",
                "mensagem": None,
                "resumo": {
                    "total_treinos": len(atividades),
                    "ultima_atividade": atividades[-1]["nome_atividade"] if atividades else None
                },
                "analise": resultado
            }

        except Exception as erro:
            return {
                "status": "fallback",
                "mensagem": "Análise indisponível no momento.",
                "resumo": {
                    "total_treinos": len(atividades),
                    "ultima_atividade": atividades[-1]["nome_atividade"] if atividades else None,
                    "erro": str(erro)
                },
                "analise": None
            }
    # ==========================================
    # CADASTRO
    # ==========================================
    def cadastrar_atividade(self, payload):

        try:
            service_validacao_atividade().validar(
                payload,
                self.db
            )

            service_banco = service_atividades_realizadas(self.db)

            atividade = service_banco.salvar(payload)

            return {
                "status": "ok",
                "atividade": {
                    "funcional": atividade.funcional,
                    "codigo_atividade": atividade.codigo_atividade,
                    "nome_atividade": atividade.descricao,
                    "data_hora": atividade.data_hora
                }
            }

        except HTTPException:
            raise

        except Exception as erro:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao cadastrar atividade: {str(erro)}"
            )