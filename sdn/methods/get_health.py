import json
import requests
from prettytable import PrettyTable

URL = "http://localhost:58000/api/v1/assurance/health" # Base Url for API-Requests

def run(service_ticket):
    '''Shows the last healthcheck'''
    headers={"X-Auth-Token": service_ticket}
    resp = requests.get(URL, headers=headers, verify=False)
    response_json = resp.json()
    healthcheck = response_json["response"][len(response_json["response"]) - 1]

    table = PrettyTable()

    table.field_names = [
      "Clients verbunden",
      "Clients aktiv",
      "Netzwerkgeräte verbunden",
      "Netzwerkgeräte aktiv",
      "Router verbunden",
      "Router aktiv",
      "Switches verbunden",
      "Switches aktiv",
      "Datum",
    ]
    table.align = "l"
    table.title = "Health"

    router_connected = next((x for x in healthcheck["networkDevices"]["networkDevices"] if x["deviceType"] == "Routers"), {}).get("healthyRatio")
    router_active = next((x for x in healthcheck["networkDevices"]["networkDevices"] if x["deviceType"] == "Routers"), {}).get("healthyPercentage")
    switches_connected = next((x for x in healthcheck["networkDevices"]["networkDevices"] if x["deviceType"] == "Switches"), {}).get("healthyRatio")
    switches_active = next((x for x in healthcheck["networkDevices"]["networkDevices"] if x["deviceType"] == "Switches"), {}).get("healthyPercentage")


    table.add_row([
      healthcheck["clients"]["totalConnected"],
      healthcheck["clients"]["totalPercentage"] + " %",
      healthcheck["networkDevices"]["totalDevices"],
      healthcheck["networkDevices"]["totalPercentage"] + " %",
      router_connected.split(":")[0] if isinstance(router_connected, str) else "0",
      "\033[1;32m%s\033[0m" %(router_active + " %" if isinstance(router_active, str) else "0 %") if (router_active if isinstance(router_active, str) else "0") == "100" else "\033[1;31m%s\033[0m" %router_active + " %" if isinstance(router_active, str) else "0 %",
      switches_connected.split(":")[0] if isinstance(switches_connected, str) else "0",
      "\033[1;32m%s\033[0m" %(switches_active + " %" if isinstance(switches_active, str) else "0 %") if (switches_active if isinstance(switches_active, str) else "0") == "100" else "\033[1;31m%s\033[0m" %switches_active + " %" if isinstance(switches_active, str) else "0 %",
      healthcheck["timestamp"],
    ])

    print(table)
    print("\n")