import io
from itertools import permutations
import mimetypes
import logging
import requests
import time

log = logging.getLogger(__name__)

# Permisions # read:survey_responses

auth_header = {"X-API-TOKEN": settings.API_TOKEN}

def get_response(response_id: str):
    r = requests.get(settings.BASE_URL + f"/surveys/{settings.SURVEY_URL}/responses/{response_id}" ,headers=auth_header )
    
    if r.status_code == 200:
        return r.json()

def get_survey_schema():
    r = requests.get(settings.BASE_URL + f"/surveys/{settings.SURVEY_URL}/response-schema" ,headers=auth_header )
    
    if r.status_code == 200:
        return r.json()

def result_export():

    r_body = {"format": "json", "compress": False, "sortByLastModifiedDate" : True} #, "startDate": "", "endDate": ""

    r = requests.post(settings.BASE_URL + f"/surveys/{settings.SURVEY_URL}/export-responses" ,headers=auth_header, json=r_body )

    if r.status_code != 200:
        print("error")
        return

    progress_id = r.json()["result"]["progressId"]
    
    while True:
        r = requests.get(settings.BASE_URL + f"/surveys/{settings.SURVEY_URL}/export-responses/{progress_id}" ,headers=auth_header )
        status = r.json()["result"]["status"]

        if status == "complete":
            file_id = r.json()["result"]["fileId"]
            break
        if status == "failed":
            break
        if status == "inProgress":
            time.sleep(1)

    r = requests.get(settings.BASE_URL + f"/surveys/{settings.SURVEY_URL}/export-responses/{file_id}/file" ,headers=auth_header )

    results = r.json()['responses']
    answers = []
    for result in results:
        try:
            answer = {
                "ethnicity": result["labels"]["QID12"],
                "race": result["labels"]["QID36"],
                "gender": result["labels"]["QID14"],
                "age": result["values"]["QID15_TEXT"],
                "browser": result["values"]["QID17_BROWSER"],
                "version": result["values"]["QID17_VERSION"],
                "os": result["values"]["QID17_OS"],
                "resolution": result["values"]["QID17_RESOLUTION"]
            }
            answers.append(answer)
        except KeyError:
            pass
    
    return answers
