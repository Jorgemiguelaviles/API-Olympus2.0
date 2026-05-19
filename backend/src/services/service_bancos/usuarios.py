# src/services/service_bancos/usuarios.py

from sqlalchemy.exc import SQLAlchemyError

from src.models.model_usuarios import model_usuarios


class service_usuarios:

    def __init__(self, db):
        self.db = db

    # ==========================================
    # Criar usuário
    # ==========================================
    def salvar(self, payload: dict):

        try:

            novo_usuario = model_usuarios(

                usuario=payload.get("usuario"),
                senha_hash=payload.get("senha_hash"),
                nome=payload.get("nome"),
                usuario_root=payload.get("usuario_root", False),
                usuario_ativado=payload.get("usuario_ativado", True)
            )

            self.db.add(novo_usuario)
            self.db.commit()
            self.db.refresh(novo_usuario)

            return {
                "funcional": novo_usuario.funcional,
                "usuario": novo_usuario.usuario,
                "nome": novo_usuario.nome,
                "usuario_root": novo_usuario.usuario_root,
                "usuario_ativado": novo_usuario.usuario_ativado
            }

        except SQLAlchemyError as erro:

            self.db.rollback()

            raise Exception(
                f"Erro ao salvar usuário no banco: {str(erro)}"
            )

    # ==========================================
    # Listar usuários (paginação)
    # ==========================================
    def listar_usuarios(self, page: int):

        if page < 1:
            page = 1

        limit = 10
        offset = (page - 1) * limit

        usuarios = (
            self.db.query(model_usuarios)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [
            {
                "funcional": u.funcional,
                "usuario": u.usuario,
                "nome": u.nome,
                "usuario_root": u.usuario_root,
                "usuario_ativado": u.usuario_ativado
            }
            for u in usuarios
        ]