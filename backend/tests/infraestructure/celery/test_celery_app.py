# tests/infraestructure/celery/test_celery_app.py

from src.infraestructure.celery.celery_app import (
    celery_app
)


# ==========================================
# CELERY INSTANCE
# ==========================================
def test_celery_instance_name():

    assert celery_app.main == "olympus"


# ==========================================
# BROKER URL
# ==========================================
def test_celery_broker_url():

    assert (
        celery_app.conf.broker_url
        == "redis://localhost:6379/0"
    )


# ==========================================
# RESULT BACKEND
# ==========================================
def test_celery_result_backend():

    assert (
        celery_app.conf.result_backend
        == "redis://localhost:6379/0"
    )


# ==========================================
# SERIALIZER
# ==========================================
def test_celery_serializer():

    assert (
        celery_app.conf.task_serializer
        == "json"
    )

    assert (
        celery_app.conf.result_serializer
        == "json"
    )


# ==========================================
# ACCEPT CONTENT
# ==========================================
def test_celery_accept_content():

    assert (
        celery_app.conf.accept_content
        == ["json"]
    )


# ==========================================
# TIMEZONE
# ==========================================
def test_celery_timezone():

    assert (
        celery_app.conf.timezone
        == "America/Sao_Paulo"
    )


# ==========================================
# ENABLE UTC
# ==========================================
def test_celery_enable_utc():

    assert (
        celery_app.conf.enable_utc
        is True
    )


# ==========================================
# INCLUDED TASKS
# ==========================================
def test_celery_include_tasks():

    includes = (
        celery_app.conf.include
    )

    assert (
        "src.infraestructure.tasks.task_analise_ia"
        in includes
    )