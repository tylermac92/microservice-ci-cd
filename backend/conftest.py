import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-db-tests",
        action="store_true",
        default=False,
        help="run DB integration tests",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "dbtest: mark test as requiring the database")
