# src/services/service_seguranca/limite_login.py

from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import HTTPException


class service_brute_force:

    def __init__(self):

        self.attempts = defaultdict(lambda: {
            "count": 0,
            "blocked_until": None
        })

        self.MAX_ATTEMPTS = 5
        self.BLOCK_MINUTES = 15

    def verificar_bloqueio(self, usuario: str):

        data = self.attempts[usuario]

        if data["blocked_until"] and datetime.utcnow() < data["blocked_until"]:
            raise HTTPException(
                status_code=429,
                detail="Muitas tentativas. Usuário temporariamente bloqueado."
            )

    def registrar_falha(self, usuario: str):

        data = self.attempts[usuario]

        data["count"] += 1

        if data["count"] >= self.MAX_ATTEMPTS:

            data["blocked_until"] = datetime.utcnow() + timedelta(
                minutes=self.BLOCK_MINUTES
            )

            data["count"] = 0

    def reset(self, usuario: str):

        self.attempts[usuario] = {
            "count": 0,
            "blocked_until": None
        }
        
brute_force_instance = service_brute_force()