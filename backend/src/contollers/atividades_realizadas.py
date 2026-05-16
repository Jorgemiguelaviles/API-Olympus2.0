from fastapi import HTTPException

from src.services.validadores.valida_atividades_realizadas import service_validacao_atividade
from src.services.service_bancos.atividades_existentes import (
    service_atividades
)


class controller_atividades_realizadas:

    def __init__(self, db):
        self.db = db


    # ==========================================
    # Buscar todas as atividades realizadas
    # ==========================================
    def buscar_todas_atividades(self):

        try:
            
            service = service_atividades(
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

            service = service_atividades(
                self.db
            )

            atividades = service.get_recupera_atividades_por_funcional(
                funcional
            )

            if not atividades:

                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma atividade encontrada para este funcional."
                )

            return atividades

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
                payload
            )

            print("Validação bem-sucedida para o payload:", payload)


            # ==========================
            # 2 - Persistir no banco
            # ==========================
            service_banco = service_atividades(
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
            


