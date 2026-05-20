from pydantic import BaseModel, ConfigDict, Field


# ==========================================
# RESPONSE - ATIVIDADE DISPONÍVEL
# ==========================================
class AtividadeExistenteResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    codigo_atividade: str = Field(
        ...,
        example="musculacao-001"
    )

    nome_atividade: str = Field(
        ...,
        example="Musculação"
    )


# ==========================================
# PAYLOAD - CRIAR OPÇÃO
# ==========================================
class AtividadeCriacaoOpcaoSchema(BaseModel):

    descricao: str = Field(
        ...,
        min_length=3,
        example="Natação"
    )


# ==========================================
# RESPONSE - OPÇÃO CRIADA
# ==========================================
class AtividadeOpcaoResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    codigo_atividade: str = Field(
        ...,
        example="natacao-001"
    )

    nome_atividade: str = Field(
        ...,
        example="Natação"
    )