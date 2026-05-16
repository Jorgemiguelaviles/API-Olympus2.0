from src.models.model_atividade import model_atividades


class service_atividades:

    def __init__(self, db):
        self.db = db


    def get_recupera_todas_atividades(self):

        activities = self.db.query(
            model_atividades
        ).all()

        return activities