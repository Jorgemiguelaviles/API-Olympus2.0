import logging

from fastapi import HTTPException

from src.infraestructure.tasks.task_analise_ia import (
    gerar_analise_ia_task
)

from src.services.validadores.valida_atividades_realizadas import (
    service_validacao_atividade
)

from src.services.service_bancos.atividades_realizadas import (
    service_atividades_realizadas
)


logger = logging.getLogger(__name__)


class controller_atividades_realizadas:


    # ==========================================
    # CONSTRUTOR
    # ==========================================
    def __init__(self, db):

        self.db = db


    # ==========================================
    # SERIALIZA
    # ==========================================
    @staticmethod
    def serializa_atividade(atividade):

        return {

            "funcional":
            atividade["funcional"]
            if isinstance(atividade, dict)
            else atividade.funcional,

            "codigo_atividade":
            atividade["codigo_atividade"]
            if isinstance(atividade, dict)
            else atividade.codigo_atividade,

            "nome_atividade":
            atividade.get("descricao")
            if isinstance(atividade, dict)
            else atividade.descricao,

            "data_hora":
            atividade["data_hora"]
            if isinstance(atividade, dict)
            else atividade.data_hora
        }


    # ==========================================
    # BUSCAR TODAS
    # ==========================================
    def buscar_todas_atividades(self):

        try:

            service = (
                service_atividades_realizadas(
                    self.db
                )
            )

            atividades = (
                service.get_recupera_todas_atividades()
            )

            if not atividades:

                raise HTTPException(
                    status_code=404,
                    detail="Nenhuma atividade encontrada."
                )

            return [
                self.serializa_atividade(a)
                for a in atividades
            ]

        except HTTPException:
            raise

        except Exception as erro:

            logger.exception(
                "Erro ao buscar atividades."
            )

            raise HTTPException(
                status_code=500,
                detail=str(erro)
            )


    # ==========================================
    # BUSCAR POR FUNCIONAL
    # ==========================================
    def buscar_por_funcional(
        self,
        funcional: int
    ):

        try:

            service = (
                service_atividades_realizadas(
                    self.db
                )
            )

            atividades = (
                service
                .get_recupera_atividades_por_funcional(
                    funcional
                )
            )

            if not atividades:

                raise HTTPException(
                    status_code=404,
                    detail=(
                        "Nenhuma atividade encontrada."
                    )
                )

            atividades_formatadas = [

                self.serializa_atividade(a)

                for a in atividades
            ]

            # ==========================================
            # DISPARA TASK
            # ==========================================
            task = (
                gerar_analise_ia_task.delay(
                    atividades_formatadas
                )
            )

            logger.info(
                "Task criada: %s",
                task.id
            )

            return {

                "atividades":
                atividades_formatadas,

                "analise_ia": {

                    "task_id": task.id,

                    "status":
                    "processando",

                    "endpoint_consulta":
                    f"/analise-ia/analise/{task.id}"
                }
            }

        except HTTPException:
            raise

        except Exception as erro:

            logger.exception(
                "Erro ao buscar funcional."
            )

            raise HTTPException(
                status_code=500,
                detail=str(erro)
            )


    # ==========================================
    # CADASTRAR
    # ==========================================
    def cadastrar_atividade(
        self,
        payload
    ):

        try:

            service_validacao_atividade().validar(
                payload,
                self.db
            )

            service_banco = (
                service_atividades_realizadas(
                    self.db
                )
            )

            atividade = (
                service_banco.salvar(payload)
            )

            return {

                "status": "ok",

                "atividade":
                self.serializa_atividade(
                    atividade
                )
            }

        except HTTPException:
            raise

        except Exception as erro:

            logger.exception(
                "Erro ao cadastrar."
            )

            raise HTTPException(
                status_code=500,
                detail=str(erro)
            )