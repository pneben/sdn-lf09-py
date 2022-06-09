import json
import requests

URL = "http://localhost:58000/api/v1/ticket" # Base Url for API-Requests

def run(username, password):
    '''
    Gets the Service Ticket (Auth Key)
    Returns serviceTicket
    '''
    headers={
      "content-type": "application/json"
    }
    body={
      "username": username,
      "password": password,
    }
    resp = requests.post(URL, json.dumps(body), headers=headers, verify=False)
    response_json = resp.json()
    service_ticket = response_json["response"]["serviceTicket"]

    return service_ticket
