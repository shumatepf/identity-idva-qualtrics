import logging
import requests
import time

from qualtrix import settings, error

log = logging.getLogger(__name__)

# Permisions # read:survey_responses

auth_header = {"X-API-TOKEN": settings.API_TOKEN}


def get_response(response_id: str):
    r = requests.get(
        settings.BASE_URL + f"/surveys/{settings.SURVEY_ID}/responses/{response_id}",
        headers=auth_header,
    )
    if r.status_code == 200:
        return r.json()


def get_survey_schema():
    r = requests.get(
        settings.BASE_URL + f"/surveys/{settings.SURVEY_ID}/response-schema",
        headers=auth_header,
    )

    if r.status_code == 200:
        return r.json()


def result_export():
    r_body = {
        "format": "json",
        "compress": False,
        "sortByLastModifiedDate": True,
    }

    r = requests.post(
        settings.BASE_URL + f"/surveys/{settings.SURVEY_ID}/export-responses",
        headers=auth_header,
        json=r_body,
    )

    if r.status_code != 200:
        return

    progress_id = r.json()["result"]["progressId"]

    while True:
        r = requests.get(
            settings.BASE_URL
            + f"/surveys/{settings.SURVEY_ID}/export-responses/{progress_id}",
            headers=auth_header,
        )
        status = r.json()["result"]["status"]

        if status == "complete":
            file_id = r.json()["result"]["fileId"]
            break
        if status == "failed":
            break
        if status == "inProgress":
            time.sleep(1)

    r = requests.get(
        settings.BASE_URL
        + f"/surveys/{settings.SURVEY_ID}/export-responses/{file_id}/file",
        headers=auth_header,
    )

    results = r.json()["responses"]
    answers = []
    for result in results:
        try:
            answer = get_answer_from_result(result)
            answers.append(answer)
        except KeyError:
            pass

    return answers


def delete_session(session_id: str):
    """
    POST /surveys/{surveyId}/sessions/{sessionId}
    body {
        "close": "true"
    }
    """
    r_body = {"close": "true"}

    url = settings.BASE_URL + f"/surveys/{settings.SURVEY_ID}/sessions/{session_id}"
    r = requests.post(url, headers=auth_header, json=r_body)

    if r.status_code == 200:
        return r.json()


def finalize_session(session_id: str, response_id: str):
    """
    Business logic for ending session, pulling response, and posting to gdrive
    """
    if not delete_session(session_id):
        raise error.QualtricsError("Not Found sessionId")

    # The session deletion api attempts to delete a session, must poll for a response
    response = ""
    for i in range(5):
        response = get_response(response_id)
        if response:
            break
        else:
            log.warn(f"Response from id {response_id} not found, trying again.")
        time.sleep(2)
    survey_answers = {"status": "", "response": {}}

    if not response or not response["meta"]["httpStatus"] == "200 - OK":
        raise error.QualtricsError("Survey response not found")

    result = response["result"]
    values = result["values"]

    # Assign survey response status
    # Qualtrics API returns poorly documented boolean as string - unsure if it returns anything else
    survey_answers["status"] = "Complete" if values["finished"] else "Incomplete"

    answer = get_answer_from_result(result)

    survey_answers["response"] = answer

    return survey_answers


def get_answer_from_result(result):
    """
    Helper function to get desired values from a result
    """
    return {
        "ethnicity": result["labels"]["QID12"],
        "race": result["labels"]["QID36"],
        "gender": result["labels"]["QID14"],
        "age": result["values"]["QID15_TEXT"],
        "browser": result["values"]["QID17_BROWSER"],
        "version": result["values"]["QID17_VERSION"],
        "os": result["values"]["QID17_OS"],
        "resolution": result["values"]["QID17_RESOLUTION"],
    }
