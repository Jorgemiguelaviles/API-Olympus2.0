from celery import Celery

celery_app = Celery(
    "olympus",
    include=[
        "src.infraestructure.tasks.task_analise_ia"
    ]
)

celery_app.conf.broker_url = (
    "redis://localhost:6379/0"
)

celery_app.conf.result_backend = (
    "redis://localhost:6379/0"
)

celery_app.conf.task_serializer = "json"
celery_app.conf.result_serializer = "json"

celery_app.conf.accept_content = [
    "json"
]

celery_app.conf.timezone = (
    "America/Sao_Paulo"
)

celery_app.conf.enable_utc = True