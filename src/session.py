import logging
from .models import Client
from .utils import normcase_email
from imap_tools import BaseMailBox, MailBox
from imaplib import IMAP4
from safe_environ import MissingEnvVar, from_env
from typing import Iterator, List, Tuple

logger = logging.getLogger(__name__)


def sessions(clients: List[Client]) -> Iterator[Tuple[Client, BaseMailBox]]:
    for client in clients:
        try:
            lookup = (normcase_email(client.account) + "_password").upper()
            mailbox = MailBox(client.mailbox).login(client.account, from_env(lookup))
            logger.info("Client authenticated as %s", client.account)
            yield client, mailbox

        except MissingEnvVar as err:
            logger.error("Login failure for account %s: %s", client.account, err)

        except IMAP4.error as err:
            logger.error("IMAP error for account %s: %s", client.account, err)
