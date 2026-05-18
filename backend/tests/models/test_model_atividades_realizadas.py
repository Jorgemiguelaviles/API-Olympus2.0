from sqlalchemy import (
    BigInteger,
    String,
    TIMESTAMP
)

from src.models.model_atividades_realizadas import (
    model_atividades_realizadas
)


# ====================================================
# Nome da tabela
# ====================================================

def test_nome_tabela():

    assert (
        model_atividades_realizadas.__tablename__
        == "atividade_realizada"
    )


# ====================================================
# Primary key
# ====================================================

def test_primary_key():

    coluna = (
        model_atividades_realizadas
        .id_atividade_realizada
        .property
        .columns[0]
    )

    assert coluna.primary_key is True


# ====================================================
# Campo funcional
# ====================================================

def test_coluna_funcional():

    coluna = (
        model_atividades_realizadas
        .funcional
        .property
        .columns[0]
    )

    assert isinstance(
        coluna.type,
        BigInteger
    )

    assert coluna.nullable is False


# ====================================================
# Campo codigo_atividade
# ====================================================

def test_coluna_codigo_atividade():

    coluna = (
        model_atividades_realizadas
        .codigo_atividade
        .property
        .columns[0]
    )

    assert isinstance(
        coluna.type,
        BigInteger
    )

    assert coluna.nullable is False


# ====================================================
# Foreign key
# ====================================================

def test_foreign_key():

    coluna = (
        model_atividades_realizadas
        .codigo_atividade
        .property
        .columns[0]
    )

    foreign_keys = list(
        coluna.foreign_keys
    )

    assert len(
        foreign_keys
    ) == 1

    fk = foreign_keys[0]

    assert (
        str(fk.target_fullname)
        == "atividade.codigo_atividade"
    )


# ====================================================
# Campo data_hora
# ====================================================

def test_coluna_data_hora():

    coluna = (
        model_atividades_realizadas
        .data_hora
        .property
        .columns[0]
    )

    assert isinstance(
        coluna.type,
        TIMESTAMP
    )

    assert coluna.nullable is False


# ====================================================
# Campo descricao
# ====================================================

def test_coluna_descricao():

    coluna = (
        model_atividades_realizadas
        .descricao
        .property
        .columns[0]
    )

    assert isinstance(
        coluna.type,
        String
    )


# ====================================================
# Relationship
# ====================================================

def test_relationship_atividade():

    relationship = (
        model_atividades_realizadas
        .atividade
        .property
    )

    assert (
        relationship.key
        == "atividade"
    )


# ====================================================
# Instanciação
# ====================================================

def test_instanciar_model():

    model = (
        model_atividades_realizadas(
            funcional=123456789,
            codigo_atividade=1,
            descricao="Corrida"
        )
    )

    assert model.funcional == 123456789
    assert model.codigo_atividade == 1
    assert model.descricao == "Corrida"