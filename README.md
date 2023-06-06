# identity-idva-qualtrics

The IDVA Qualtrics Interface Microservice is a Python FAST API web app that allows for cloud foundry apps to interface to the Qualtrics API.

## Configuration
Survey and authentication settings are configured in `settings.py`. App configuration settings are pulled from environment variables.

## Endpoints

`POST /bulk-responses`

Fetches bulk responses.

`POST /response/{responseId}`

Fetches individual response.

`POST /survey-schema`

Fetches survey schema.

`POST /finalize-session`

Request body:
```
{
    "sessionId": "",
    "responseId": ""
}
```
Ends an individual session and fetches response.
