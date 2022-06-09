import json
import requests
from prettytable import PrettyTable

URL = "http://localhost:58000/api/v1/network-device" # Base Url for API-Requests

def run(service_ticket):
    '''Get the Network Devices from registered in the Network Controller'''
    headers={"X-Auth-Token": service_ticket}
    resp = requests.get(URL, headers=headers, verify=False)
    response_json = resp.json()
    network_devices = response_json["response"]

    table = PrettyTable()

    table.field_names = ["Hostname", "IP-Adresse", "MAC-Adresse", "Produkt", "Erreichbar", "Laufzeit"]
    table.align = "l"
    table.title = "Netzwerkgeräte"
    for device in network_devices:
        table.add_row([device["hostname"], device["managementIpAddress"], device["macAddress"], device["productId"], "\033[1;32m%s\033[0m" %device["reachabilityStatus"] if device["reachabilityStatus"] == "Reachable" else "\033[1;31m%s\033[0m" %device["reachabilityStatus"], device["upTime"]])

    print(table)
    print("\n")