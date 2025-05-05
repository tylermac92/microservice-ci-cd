import pytest
from sqlalchemy import text
from app import create_app

pytestmark = pytest.mark.dbtest

@pytest.fixture
def app():
    return create_app()

def test_database_connection(app):
    with app.app_context():
        conn = app.db_engine.connect()
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
