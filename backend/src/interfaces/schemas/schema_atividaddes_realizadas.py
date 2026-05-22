from datetime import datetime
from typing import (
    Optional,
    List
)

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


# ==========================================
# ATIVIDADE
# ==========================================
class AtividadeResponseSchema(
    BaseModel
):

    model_config = ConfigDict(
        from_attributes=True
    )

    funcional: int = Field(
        description=(
            "Número funcional do usuário"
        )
    )

    codigo_atividade: str = Field(
        description=(
            "Código identificador da atividade"
        )
    )

    nome_atividade: str = Field(
        description=(
            "Nome ou descrição da atividade"
        )
    )

    data_hora: datetime = Field(
        description=(
            "Data e hora do registro"
        )
    )


# ==========================================
# TASK IA
# ==========================================
class AnaliseIATaskSchema(
    BaseModel
):

    task_id: str = Field(
        description=(
            "ID da task Celery"
        )
    )

    status: str = Field(
        description=(
            "Status inicial da task"
        )
    )

    endpoint_consulta: str = Field(
        description=(
            "Endpoint para consultar status"
        )
    )


# ==========================================
# RESPONSE GET FUNCIONAL
# ==========================================
class AtividadesPraticadasResponseSchema(
    BaseModel
):

    atividades: List[
        AtividadeResponseSchema
    ] = Field(
        description=(
            "Lista de atividades praticadas"
        )
    )

    analise_ia: (
        AnaliseIATaskSchema
    ) = Field(
        description=(
            "Informações da task de análise IA"
        )
    )


# ==========================================
# POST RESPONSE
# ==========================================
class CadastroAtividadeResponseSchema(
    BaseModel
):

    status: str = Field(
        description=(
            "Status da operação"
        )
    )

    atividade: (
        AtividadeResponseSchema
    ) = Field(
        description=(
            "Dados da atividade cadastrada"
        )
    )


# ==========================================
# CREATE PAYLOAD
# ==========================================
class AtividadeCriacaoSchema(
    BaseModel
):

    model_config = ConfigDict(

        json_schema_extra={

            "example": {

                "codigo_atividade":
                "SUPINO-001",

                "descricao":
                "Treino de peito"
            }
        }
    )

    codigo_atividade: str = Field(
        ...,
        min_length=1,
        description=(
            "Código único da atividade"
        )
    )

    descricao: Optional[str] = Field(
        default=None,
        description=(
            "Descrição da atividade"
        )
    )
