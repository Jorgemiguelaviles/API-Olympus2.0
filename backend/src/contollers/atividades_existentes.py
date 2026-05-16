from src.services.service_bancos.atividades_existentes import service_atividades


class controller_atividade_existente:

    def __init__(self, db):
        self.db = db


    def gerencia_atividades(self):

        service = service_atividades(
            self.db
        )

        return service.get_recupera_todas_atividades()