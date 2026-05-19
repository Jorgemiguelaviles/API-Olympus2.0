from fastapi import HTTPException

from src.services.service_bancos.atividades_existentes import (
    service_atividades
)

from src.services.validadores.valida_nova_atividade import (
    service_validacao_atividade
)


class controller_atividade_existente:

    def __init__(self, db):

        self.db = db

        self.service_banco = service_atividades(db)

        self.service_validacao = service_validacao_atividade()

    # ==========================================
    # BUSCAR ATIVIDADES
    # ==========================================
    def busca_atividades(self):

        try:

            atividades = self.service_banco.buscar_todas_atividades()

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
    # CADASTRAR ATIVIDADE
    # ==========================================
    def cadastrar_atividade(self, payload):

        try:

            self.service_validacao.validar_cadastro(
                payload,
                self.db
            )

            payload["descricao"] = (
                payload.get("descricao")
                .strip()
                .upper()
            )

            return self.service_banco.cadastrar_atividade(
                payload
            )

        except HTTPException:
            raise

        except Exception as erro:

            raise HTTPException(
                status_code=500,
                detail=f"Erro ao cadastrar atividade: {str(erro)}"
            )