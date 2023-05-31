"""
qualtrix rest api
"""

import base64 as base64decoder
import io
import logging

import fastapi
from fastapi import Body, Request
from pydantic import BaseModel

from . import client

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
    return client.finalize_session(request.sessionId, request.responseId)
