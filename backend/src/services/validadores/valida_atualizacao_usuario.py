import re

from fastapi import HTTPException


class service_validacao_atualizacao_usuario:

    # ==========================================
    # VALIDAR UPDATE USUÁRIO
    # ==========================================
    def validar_atualizações(
        self,
        payload: dict
    ):

        dados_atualizacao = {}

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

            dados_atualizacao["usuario"] = usuario

        # ==========================================
        # SENHA
        # ==========================================
        senha = payload.get("senha")

        if senha is not None:

            regex_senha = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'

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