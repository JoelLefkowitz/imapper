import logging
from imaplib import IMAP4
from typing import Dict, List

# pylint: disable=E0401
from imap_tools import U

from .models import Client
from .session import sessions
from .utils import increment_dict, intervals

logger = logging.getLogger(__name__)


BATCH_COUNT = 100
BATCH_LIMIT = 100


def fetch_senders(clients: List[Client]) -> None:
    for client, _mailbox in sessions(clients):
        with _mailbox as mailbox:
            try:
                senders = {}  # type: Dict[str, int]

                for (start, end) in intervals(1, BATCH_LIMIT, BATCH_COUNT):
                    ids = U(start, end)
                    logger.info("Fetching messages with uid in range: %s", ids)

                    matches = mailbox.fetch(
                        ids,
                        headers_only=True,
                        limit=BATCH_LIMIT,
                        bulk=True,
                    )

                    for i in matches:
                        increment_dict(senders, i.from_)

                logger.info(dict(sorted(senders.items(), key=lambda x: x[1])))

            except IMAP4.error as err:
                logger.error("IMAP error for account %s: %s", client.account, err)
