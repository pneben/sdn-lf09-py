'''
Main File
'''
import inquirer
from sdn.methods import get_network_devices, get_ticket, get_hosts, get_host_by_ip, get_health

credentialsQuestions = [
    inquirer.Text('username', message="Username"),
    inquirer.Password('password', message="Password")
]

methodDictionary = {
    "Zeige Netzwerkgeräte": get_network_devices.run,
    "Zeige Hosts": get_hosts.run,
    "Suche Host nach IP": get_host_by_ip.run,
    "Healthcheck": get_health.run,
}

methodSelection = [
    inquirer.List('method',
                    message="Welche Methode soll ausgeführt werden?",
                    choices=list(methodDictionary.keys()),
                ),
]

def main():
    '''Main entry of program'''
    running = True
    service_ticket = None

    while service_ticket is None or len(service_ticket) == 0:
        credentials = inquirer.prompt(credentialsQuestions)
        service_ticket = get_ticket.run(credentials["username"], credentials["password"])

    while running:
        answers = inquirer.prompt(methodSelection)
        methodDictionary[answers['method']](service_ticket)
 