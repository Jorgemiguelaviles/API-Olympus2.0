from sqlalchemy import (
    BigInteger,
    String
)

from src.models.model_atividades import (
    model_atividades
)


# ====================================================
# Nome da tabela
# ====================================================

def test_nome_tabela():

    assert (
        model_atividades.__tablename__
        == "atividade"
    )


# ====================================================
# Primary key
# ====================================================

def test_primary_key():

    coluna = (
        model_atividades
        .codigo_atividade
        .property
        .columns[0]
    )

    assert coluna.primary_key is True


# ====================================================
# Tipo da PK
# ====================================================

def test_tipo_codigo_atividade():

    coluna = (
        model_atividades
        .codigo_atividade
        .property
        .columns[0]
    )

    assert isinstance(
        coluna.type,
        BigInteger
    )


# ====================================================
# Autoincrement
# ====================================================

def test_codigo_atividade_autoincrement():

    coluna = (
        model_atividades
        .codigo_atividade
        .property
        .columns[0]
    )

    assert coluna.autoincrement is True


# ====================================================
# Campo nome_atividade
# ====================================================

def test_coluna_nome_atividade():

    coluna = (
        model_atividades
        .nome_atividade
        .property
        .columns[0]
    )

    assert isinstance(
        coluna.type,
        String
    )

    assert coluna.type.length == 50

    assert coluna.nullable is False


# ====================================================
# Unique constraint
# ====================================================

def test_nome_atividade_unique():

    coluna = (
        model_atividades
        .nome_atividade
        .property
        .columns[0]
    )

    assert coluna.unique is True


# ====================================================
# Relationship
# ====================================================

def test_relationship_atividades_realizadas():

    rel = (
        model_atividades
        .atividades_realizadas
        .property
    )

    assert (
        rel.key
        == "atividades_realizadas"
    )


# ====================================================
# Instanciação
# ====================================================

def test_instanciar_model():

    atividade = model_atividades(
        nome_atividade="Corrida"
    )

    assert (
        atividade.nome_atividade
        == "Corrida"
    )