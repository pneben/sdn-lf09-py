import json
import requests
from prettytable import PrettyTable

URL = "http://localhost:58000/api/v1/host" # Base Url for API-Requests

def run(service_ticket):
    '''Get the Hosts in the network'''
    headers={"X-Auth-Token": service_ticket}
    resp = requests.get(URL, headers=headers, verify=False)
    response_json = resp.json()
    network_devices = response_json["response"]

    table = PrettyTable()

    table.field_names = ["Hostname", "IP-Adresse", "MAC-Adresse", "Verbundenes Gerät", "Ping"]
    table.align = "l"
    table.title = "Hosts"
    for device in network_devices:
        table.add_row([
          device["hostName"],
          device["hostIp"],
          device["hostMac"],
          device["connectedNetworkDeviceName"],
          "\033[1;32m%s\033[0m" %device["pingStatus"] if device["pingStatus"] == "SUCCESS" else "\033[1;31m%s\033[0m" %device["pingStatus"]
        ])

    print(table)
    print("\n")