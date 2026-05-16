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