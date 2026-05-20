# src/services/service_bancos/usuarios.py

from sqlalchemy.exc import SQLAlchemyError

from src.models.model_usuarios import model_usuarios


class service_usuarios:

    def __init__(self, db):
        self.db = db

    # ==========================================
    # CRIAR USUÁRIO
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
    # LISTAR USUÁRIOS
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

    # ==========================================
    # ALTERAR CONFIGURAÇÃO USUÁRIO
    # ==========================================
    def alterar_configuracao_usuario(
        self,
        funcional: int,
        campo: str
    ):

        try:

            usuario = (
                self.db.query(model_usuarios)
                .filter(
                    model_usuarios.funcional == funcional
                )
                .first()
            )

            # ==========================================
            # TOGGLE BOOLEAN
            # ==========================================
            valor_atual = getattr(
                usuario,
                campo
            )

            novo_valor = not valor_atual

            setattr(
                usuario,
                campo,
                novo_valor
            )

            self.db.commit()

            self.db.refresh(usuario)

            return {
                "message": f"{campo} atualizado com sucesso.",
                "funcional": usuario.funcional,
                campo: novo_valor
            }

        except SQLAlchemyError as erro:

            self.db.rollback()

            raise Exception(
                f"Erro ao alterar configuração do usuário: {str(erro)}"
            )

    # ==========================================
    # ATUALIZAR USUÁRIO
    # ==========================================
    def atualizar_usuario(
        self,
        funcional: int,
        payload: dict
    ):

        try:

            usuario = (
                self.db.query(model_usuarios)
                .filter(
                    model_usuarios.funcional == funcional
                )
                .first()
            )

            # ==========================================
            # UPDATE DINÂMICO
            # ==========================================
            for chave, valor in payload.items():

                # ignora campos vazios
                if valor is None:
                    continue

                setattr(
                    usuario,
                    chave,
                    valor
                )

            self.db.commit()

            self.db.refresh(usuario)

            return {
                "funcional": usuario.funcional,
                "usuario": usuario.usuario,
                "nome": usuario.nome,
                "usuario_root": usuario.usuario_root,
                "usuario_ativado": usuario.usuario_ativado
            }

        except SQLAlchemyError as erro:

            self.db.rollback()

            raise Exception(
                f"Erro ao atualizar usuário: {str(erro)}"
            )