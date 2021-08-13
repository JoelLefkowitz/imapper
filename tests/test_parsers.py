from src.models import Client, Folder
from src.parsers import parse_clients


def test_parse_clients() -> None:
    assert parse_clients(
        [
            {
                "account": "joellefkowitz@hotmail.com",
                "folders": [{"name": "Amazon", "patterns": ["amazon"]}],
                "mailbox": "imap-mail.outlook.com",
            }
        ]
    ) == [
        Client(
            mailbox="imap-mail.outlook.com",
            account="joellefkowitz@hotmail.com",
            folders=[Folder(name="Amazon", patterns=["amazon"])],
        )
    ]
