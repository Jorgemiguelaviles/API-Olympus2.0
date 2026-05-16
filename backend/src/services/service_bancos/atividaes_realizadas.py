from src.models.model_atividade import (
    model_atividades
)


class service_atividades:

    def __init__(self, db):
        self.db = db


    # ==========================================
    # Buscar todas as atividades
    # ==========================================
    def buscar_todas_atividades(self):
        print('Buscando todas as atividades...')

        atividades = self.db.query(
            model_atividades
        ).all()

        return atividades

