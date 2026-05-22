from src.infraestructure.celery.celery_app import (
    celery_app
)

from src.services.service_APIs.service_gemini import (
    service_gemini
)


@celery_app.task
def gerar_analise_ia_task(
    atividades_formatadas
):

    descricoes = [

        a["nome_atividade"]

        for a in atividades_formatadas

        if a.get("nome_atividade")
    ]

    resultado = (
        service_gemini().analisa_dados(
            dados_usuario=descricoes,
            prompt_usuario=(
                "Analise a evolução física."
            )
        )
    )

    return resultado