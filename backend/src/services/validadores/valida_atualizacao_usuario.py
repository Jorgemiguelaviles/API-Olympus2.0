import re

from fastapi import HTTPException

from src.models.model_usuarios import (
    model_usuarios
)


class service_validacao_atualizacao_usuario:

    # ==========================================
    # VALIDAR UPDATE USUÁRIO
    # ==========================================
    def validar_atualizacoes(
        self,
        payload: dict,
        db
    ):

        # ==========================================
        # VALIDAR FUNCIONAL
        # ==========================================
        funcional = payload.get("funcional")

        if funcional is None:

            raise HTTPException(
                status_code=400,
                detail="Funcional é obrigatória."
            )

        # ==========================================
        # VALIDAR NUMÉRICO
        # ==========================================
        if not str(funcional).isdigit():

            raise HTTPException(
                status_code=400,
                detail="A funcional deve ser numérica."
            )

        funcional = int(funcional)

        # ==========================================
        # VALIDAR EXISTÊNCIA
        # ==========================================
        usuario_existente = db.query(
            model_usuarios
        ).filter(
            model_usuarios.funcional == funcional
        ).first()

        if not usuario_existente:

            raise HTTPException(
                status_code=404,
                detail="Usuário não encontrado."
            )

        # ==========================================
        # NOME
        # ==========================================
        nome = payload.get("nome")

        if nome is not None:

            nome = nome.strip()

            if len(nome) < 3:

                raise HTTPException(
                    status_code=400,
                    detail="Nome deve possuir ao menos 3 caracteres."
                )

            dados_atualizacao["nome"] = nome

        # ==========================================
        # EMAIL
        # ==========================================
        usuario = payload.get("usuario")

        if usuario is not None:

            usuario = usuario.strip()

            regex_email = r'^[\w\.-]+@[\w\.-]+\.\w+$'

            if not re.match(regex_email, usuario):

                raise HTTPException(
                    status_code=400,
                    detail="Formato de email inválido."
                )

            # ==========================================
            # EMAIL JÁ EXISTE
            # ==========================================
            email_existente = db.query(
                model_usuarios
            ).filter(
                model_usuarios.usuario == usuario,
                model_usuarios.funcional != funcional
            ).first()

            if email_existente:

                raise HTTPException(
                    status_code=400,
                    detail="Email já cadastrado."
                )

            dados_atualizacao["usuario"] = usuario

        # ==========================================
        # SENHA
        # ==========================================
        senha = payload.get("senha")

        if senha is not None:

            regex_senha = (
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)'
                r'(?=.*[^A-Za-z0-9]).{8,}$'
            )

            if not re.match(regex_senha, senha):

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Senha fraca. A senha deve conter no mínimo "
                        "8 caracteres, incluindo letra maiúscula, "
                        "minúscula, número e caractere especial."
                    )
                )

            dados_atualizacao["senha"] = senha

        # ==========================================
        # NADA ENVIADO
        # ==========================================
        if not dados_atualizacao:

            raise HTTPException(
                status_code=400,
                detail="Nenhum campo enviado para atualização."
            )

        return dados_atualizacao