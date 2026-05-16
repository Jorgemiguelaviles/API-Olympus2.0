from src.models.model_atividade import model_atividades
from src.models.model_atividade_realizada import (
    model_atividades_realizadas
)


class service_atividades:

    def __init__(self, db):
        self.db = db


    # ==========================================
    # Buscar todas as atividades realizadas
    # ==========================================
    def get_recupera_todas_atividades(self):

        atividades = self.db.query(
            model_atividades_realizadas
        ).all()

        return atividades


    # ==========================================
    # Buscar por funcional
    # ==========================================
    def get_recupera_atividades_por_funcional(
        self,
        funcional: int
    ):

        atividades = self.db.query(
            model_atividades_realizadas
        ).filter(
            model_atividades_realizadas.funcional == funcional
        ).all()

        return atividades
    


        

    def salvar(
        self,
        payload
    ):

        atividade_existente = self.db.query(
            model_atividades
        ).filter(
            model_atividades.nome_atividade == payload.get("codigo_atividade")
        ).first()


        if not atividade_existente:

            raise ValueError(
                "Atividade não encontrada."
            )


        nova_atividade = model_atividades_realizadas(
            funcional=payload.get("funcional"),
            codigo_atividade=atividade_existente.codigo_atividade,
            descricao=payload.get("descricao"),
            data_hora=payload.get("data_hora")
        )


        self.db.add(
            nova_atividade
        )

        self.db.commit()

        self.db.refresh(
            nova_atividade
        )

        return nova_atividade