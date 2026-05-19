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


    # ==========================================
    # Buscar todas as atividades realizadas
    # ==========================================
    def buscar_todas_atividades(self):

        try:
            
            service = service_atividades_realizadas(
                self.db
            )

            atividades = service.get_recupera_todas_atividades()

            if not atividades:

                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma atividade encontrada."
                )

            return atividades

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao consultar atividades: {str(erro)}"
            )


    # ==========================================
    # Buscar atividades por funcional
    # ==========================================
    def buscar_por_funcional(
        self,
        funcional: int
    ):

        try:

            service = service_atividades_realizadas(
                self.db
            )

            print('funcional', funcional)

            atividades = service.get_recupera_atividades_por_funcional(
                funcional
            )

            print(type(atividades))
            print(atividades)

            descricoes = [
                atividade["descricao"]
                for atividade in atividades
                if atividade["descricao"]
            ]

            # ==========================================
            # Carregar variáveis de ambiente
            # ==========================================

            BASE_DIR = Path(
                __file__
            ).resolve().parent.parent.parent.parent

            load_dotenv(
                dotenv_path=BASE_DIR / ".env"
            )

            chave_api = os.getenv(
                "API_KEY_GEMINI"
            )

            if chave_api and atividades:
                resultado_ia = service_gemini(chave_api).analisa_dados(
                    dados_usuario=descricoes,
                    prompt_usuario=(
                        "Analise a evolução física do usuário "
                        "com base nos treinos realizados."
                    )
                )
            
            else:
                resultado_ia = "API_KEY_GEMINI não configurada. ou nenhuma atividade encontrada."

            if not atividades:

                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma atividade encontrada para este funcional."
                )
            
            response = {
                "atividades": atividades,
                "analise_ia": resultado_ia}
            

            return response

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao consultar funcional: {str(erro)}"
            )
        
    
        

    def cadastrar_atividade(
        self,
        payload
    ):

        try:

            # ==========================
            # 1 - Validar dados
            # ==========================
            service_validacao_atividade().validar(
                payload,
                self.db
            )

            print("Validação bem-sucedida para o payload:", payload)


            # ==========================
            # 2 - Persistir no banco
            # ==========================
            service_banco = service_atividades_realizadas(
                self.db
            )

            atividade = service_banco.salvar(
                payload
            )

            return atividade


        except HTTPException:
            raise


        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao cadastrar atividade: {str(erro)}")
            


