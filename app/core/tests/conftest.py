from unittest.mock import patch
import pytest

@pytest.fixture()
def get_db():
    with patch("django.db.utils.ConnectionHandler.__getitem__") as gi:
        return gi

