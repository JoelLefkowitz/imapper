from .models import Client, Folder
from typing import Any, List


def parse_clients(clients_json: List[Any]) -> List[Client]:
    return [
        Client(
            mailbox=i["mailbox"],
            account=i["account"],
            folders=[
                Folder(name=j["name"], patterns=j["patterns"]) for j in i["folders"]
            ],
        )
        for i in clients_json
    ]
