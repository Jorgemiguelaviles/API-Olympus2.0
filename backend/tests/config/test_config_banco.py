from unittest.mock import MagicMock, patch
import importlib

import src.config.config_banco as config_banco


# ==========================================
# Reload do módulo com mocks
# ==========================================
def carregar_modulo():

    fake_env = {
        "DB_USER": "jorge",
        "DB_PASSWORD": "senha@123",
        "DB_HOST": "localhost",
        "DB_PORT": "3306",
        "DB_NAME": "olympus"
    }

    with patch("os.getenv") as mock_getenv, \
         patch("sqlalchemy.create_engine") as mock_engine, \
         patch("dotenv.load_dotenv"):

        mock_getenv.side_effect = lambda key: fake_env.get(key)

        mock_engine.return_value = MagicMock()

        importlib.reload(
            config_banco
        )

        return config_banco


def test_env_variables_loaded():

    module = carregar_modulo()

    assert module.DB_USER == "jorge"
    assert module.DB_HOST == "localhost"
    assert module.DB_PORT == "3306"
    assert module.DB_NAME == "olympus"


def test_password_encoding():

    module = carregar_modulo()

    assert module.DB_PASSWORD == "senha%40123"


def test_database_url():

    module = carregar_modulo()

    assert "mysql+pymysql://" in module.DATABASE_URL


def test_base_exists():

    module = carregar_modulo()

    assert module.Base is not None


def test_session_local_exists():

    module = carregar_modulo()

    assert module.SessionLocal is not None


def test_get_db_success():

    module = carregar_modulo()

    fake_db = MagicMock()

    with patch.object(
        module,
        "SessionLocal",
        return_value=fake_db
    ):

        generator = module.get_db()

        db = next(generator)

        assert db == fake_db

        generator.close()

        fake_db.close.assert_called_once()


def test_get_db_exception():

    module = carregar_modulo()

    fake_db = MagicMock()

    with patch.object(
        module,
        "SessionLocal",
        return_value=fake_db
    ):

        generator = module.get_db()

        next(generator)

        generator.close()

        fake_db.close.assert_called_once()