from unittest.mock import MagicMock

from src.services.service_bancos.atividades_existentes import (
    service_atividades
)

from src.models.model_atividades import (
    model_atividades
)


# ==========================================
# Deve buscar atividades com sucesso
# ==========================================
def test_buscar_todas_atividades_com_sucesso():

    # Arrange
    mock_db = MagicMock()

    retorno_mockado = [
        MagicMock(
            codigo_atividade=1,
            nome_atividade="Corrida"
        ),
        MagicMock(
            codigo_atividade=2,
            nome_atividade="Musculação"
        )
    ]

    mock_db.query.return_value.all.return_value = (
        retorno_mockado
    )

    service = service_atividades(
        mock_db
    )

    # Act
    resultado = (
        service.buscar_todas_atividades()
    )

    # Assert
    mock_db.query.assert_called_once_with(
        model_atividades
    )

    mock_db.query.return_value.all.assert_called_once()

    assert resultado == retorno_mockado


# ==========================================
# Deve retornar lista vazia
# ==========================================
def test_buscar_todas_atividades_lista_vazia():

    # Arrange
    mock_db = MagicMock()

    mock_db.query.return_value.all.return_value = []

    service = service_atividades(
        mock_db
    )

    # Act
    resultado = (
        service.buscar_todas_atividades()
    )

    # Assert
    assert resultado == []

    mock_db.query.assert_called_once_with(
        model_atividades
    )


# ==========================================
# Deve propagar erro do banco
# ==========================================
def test_buscar_todas_atividades_com_erro():

    # Arrange
    mock_db = MagicMock()

    mock_db.query.side_effect = Exception(
        "Erro no banco"
    )

    service = service_atividades(
        mock_db
    )

    # Act / Assert
    try:

        service.buscar_todas_atividades()

        assert False

    except Exception as erro:

        assert str(erro) == (
            "Erro no banco"
        )