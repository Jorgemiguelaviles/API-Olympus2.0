from src.main import app


# ==========================================
# App criada corretamente
# ==========================================
def test_app_foi_criada():

    assert app is not None


# ==========================================
# Metadados da API
# ==========================================
def test_metadata_api():

    assert app.title == (
        "Olympus API"
    )

    assert app.description == (
        "API para gerenciamento de atividades físicas"
    )

    assert app.version == (
        "1.0.0"
    )


# ==========================================
# Rotas registradas
# ==========================================
def test_rotas_registradas():

    rotas = [
        route.path
        for route in app.routes
    ]

    assert (
        "/atividades/opcoes"
        in rotas
    )

    assert (
        "/atividades/praticadas/"
        in rotas
    )

    assert (
        "/atividades/praticadas/{funcional}"
        in rotas
    )
def test_metodos_rotas():

    rotas_praticadas = [
        route
        for route in app.routes
        if route.path == "/atividades/praticadas/"
    ]

    # Deve existir GET e POST no mesmo endpoint
    metodos = set()

    for rota in rotas_praticadas:
        metodos.update(
            rota.methods
        )

    assert "GET" in metodos

    assert "POST" in metodos


    rota_opcoes = next(
        route
        for route in app.routes
        if route.path == "/atividades/opcoes"
    )

    assert "GET" in (
        rota_opcoes.methods
    )


    rota_funcional = next(
        route
        for route in app.routes
        if route.path == "/atividades/praticadas/{funcional}"
    )

    assert "GET" in (
        rota_funcional.methods
    )