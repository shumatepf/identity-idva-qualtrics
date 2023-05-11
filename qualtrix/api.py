"""
qualtrix rest api
"""

import base64 as base64decoder
import io
import logging

import fastapi
from fastapi import Body
from starlette.requests import Request

from . import client, settings

log = logging.getLogger(__name__)

router = fastapi.APIRouter()


@router.post("/bulk-responses")
async def test(surveyId: str):

    return client.result_export()

@router.post("/response")
async def test(responseId: str):

    client.get_response(responseId)

@router.post("/survey-schema")
async def test(surveyId: str):

    return client.get_survey_schema(surveyId)

