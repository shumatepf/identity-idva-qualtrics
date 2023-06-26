import sys
import json
from unittest.mock import MagicMock

from fastapi import testclient

# pylint: disable=wrong-import-position
sys.modules["qualtrix.client"] = MagicMock()
from qualtrix import main

client = testclient.TestClient(main.app)


def test_session_delete() -> None:
    """test upload endpoint"""

    response = client.post(
        "/delete-session",
        data=json.dumps({"surveyId": "1234", "sessionId": "5678"}),
    )

    assert response.status_code == 200
