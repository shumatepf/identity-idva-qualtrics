"""
qualtrix rest api
"""

import logging

import fastapi
from fastapi import HTTPException
from pydantic import BaseModel

from qualtrix import client, error

log = logging.getLogger(__name__)

router = fastapi.APIRouter()


@router.post("/bulk-responses")
async def test():

    return client.result_export()

@router.post("/response/{responseId}")
async def test(responseId: str):

    response = client.get_response(responseId)
    print(response)
    return response

@router.post("/survey-schema")
async def test():

    return client.get_survey_schema()

class SessionResponseFlow(BaseModel):
    sessionId: str
    responseId: str

@router.post("/finalize-session")
async def session(request: SessionResponseFlow):
    """
    Router for ending a session, pulling response
    """
    try:
        return client.finalize_session(request.sessionId, request.responseId)
    except error.QualtricsError as e:
        raise HTTPException(status_code=400, detail=e.args)
