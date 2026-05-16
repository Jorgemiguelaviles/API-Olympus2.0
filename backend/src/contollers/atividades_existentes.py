from src.services.service_bancos.atividades_existentes import ActivityService


class controller_atividade_existente:

    def __init__(self, db):
        self.db = db


    def get_all_activities(self):

        service = ActivityService(
            self.db
        )

        return service.get_all_activities()