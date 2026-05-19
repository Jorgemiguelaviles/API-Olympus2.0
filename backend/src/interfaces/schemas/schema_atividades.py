from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ==========================================
# RESPOSTA ATIVIDADE REALIZADA
# ==========================================
class AtividadeRespostaSchema(BaseModel):

    funcional: int

    codigo_atividade: str

    nome_atividade: Optional[str]

    data_hora: datetime

    class Config:
        from_attributes = True


# ==========================================
# RESPOSTA COM IA
# ==========================================
class AtividadeComAnaliseSchema(BaseModel):

    atividades: List[AtividadeRespostaSchema]

    analise_ia: str


# ==========================================
# RESPOSTA ATIVIDADES DISPONÍVEIS
# ==========================================
class AtividadeExistenteResponseSchema(BaseModel):

    codigo_atividade: str

    nome_atividade: str

    class Config:
        from_attributes = True


# ==========================================
# CRIAÇÃO NOVA OPÇÃO
# ==========================================
class AtividadeCriacaoOpcaoSchema(BaseModel):

    descricao: str


# ==========================================
# RESPOSTA NOVA OPÇÃO
# ==========================================
class AtividadeOpcaoResponseSchema(BaseModel):

    codigo_atividade: str

    nome_atividade: str

    class Config:
        from_attributes = True