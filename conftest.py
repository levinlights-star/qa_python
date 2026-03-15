import pytest
from main import BooksCollector

@pytest.fixture
def col():
    return BooksCollector()