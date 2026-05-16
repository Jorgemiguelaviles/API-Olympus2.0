from src.models.model_atividade import model_atividades


class ActivityService:

    def __init__(self, db):
        self.db = db


    def get_all_activities(self):

        activities = self.db.query(
            model_atividades
        ).all()

        return activities