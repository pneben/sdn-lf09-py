import json
import inquirer
import requests
from prettytable import PrettyTable

URL = "http://localhost:58000/api/v1/host/ip-address/" # Base Url for API-Requests

ipAddressQuestions = [
    inquirer.Text('ip_adress', message="IP-Adresse"),
]


def run(service_ticket):
    '''Get the Hosts in the network'''
    headers={"X-Auth-Token": service_ticket}
    
    input_resp = inquirer.prompt(ipAddressQuestions)
    if input_resp["ip_adress"] is None:
      return

    resp = requests.get(URL + input_resp["ip_adress"], headers=headers, verify=False)

    if resp.status_code == 404:
      print("\nEs wurde kein Host gefunden\n")
      return

    host = resp.json()

    table = PrettyTable()

    table.field_names = ["Hostname", "IP-Adresse", "MAC-Adresse", "Id", "Verbundenes Gerät", "Ping", "Interface", "Zuletzt geändert"]
    table.align = "l"
    table.add_row([host["hostName"], host["hostIp"], host["hostMac"], host["id"], host["connectedNetworkDeviceName"], "\033[1;32m%s\033[0m" %host["pingStatus"] if host["pingStatus"] == "SUCCESS" else "\033[1;31m%s\033[0m" %host["pingStatus"], host["connectedInterfaceName"], host["lastUpdated"]])

    print(table)
    print("\n")