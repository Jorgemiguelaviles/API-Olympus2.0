from src.models.model_atividade_realizada import (
    model_atividades_realizadas
)


class service_atividades_realizadas:

    def __init__(self, db):
        self.db = db


    # ==========================================
    # Buscar todas as atividades realizadas
    # ==========================================
    def buscar_todas_atividades(self):

        atividades = self.db.query(
            model_atividades_realizadas
        ).all()

        return atividades


    # ==========================================
    # Buscar atividades por funcional
    # ==========================================
    def buscar_por_funcional(
        self,
        funcional: int
    ):

        atividades = self.db.query(
            model_atividades_realizadas
        ).filter(
            model_atividades_realizadas.funcional == funcional
        ).all()

        return atividades