import itertools
import logging
import sched
import time
from .models import Client, Folder, FolderStats
from .session import sessions
from .utils import chunks, flatten, show_lst
from imap_tools import AND, OR, MailBox
from imaplib import IMAP4
from typing import Any, List

REPEAT_DELAY = 60 * 5
BATCH_LIMIT = 100
PATTERN_LENGTH_LIMIT = 5

logger = logging.getLogger(__name__)


def sweep_on_loop(clients: List[Client]) -> None:
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(0, 1, launch_sweep, (scheduler, clients))
    scheduler.run()


def launch_sweep(scheduler: sched.scheduler, clients: List[Client]) -> None:
    for client, _mailbox in sessions(clients):
        with _mailbox as mailbox:
            try:
                sweep_client(client, mailbox)

            except IMAP4.error as err:
                logger.error("IMAP error for account %s: %s", client.account, err)

        logger.info("Sweep completed, restarting in %d", REPEAT_DELAY)
        scheduler.enter(REPEAT_DELAY, 1, sweep_on_loop, (scheduler, clients))


def sweep_client(client: Client, mailbox: MailBox):
    before_stats = gather_stats(mailbox)

    for source_folder, target_folder in itertools.permutations(client.folders, 2):
        for pattern_set in chunks(target_folder.patterns, PATTERN_LENGTH_LIMIT):
            logger.info(
                "Attempting to move matching messages from %s to %s:",
                source_folder.name,
                target_folder.name,
            )
            move_mail(mailbox, pattern_set, source_folder, target_folder)

    after_stats = gather_stats(mailbox)

    for i, j in zip(before_stats, after_stats):
        logger.info(
            "Changes for folder %s: %d, total messages: %d",
            i.name,
            j.count - i.count,
            j.count,
        )


def move_mail(
    mailbox: MailBox,
    pattern_set: List[str],
    source_folder: Folder,
    target_folder: Folder,
) -> None:
    patterns = OR(*[AND(from_=i) for i in pattern_set])
    show_patterns = show_lst([f"from {i}" for i in pattern_set], " OR ")

    logger.info(
        "Searching for messages in %s with pattern set: %s.",
        source_folder.name,
        show_patterns,
    )

    mailbox.folder.set(source_folder.name)
    matches = mailbox.fetch(patterns, limit=BATCH_LIMIT)

    if not mailbox.folder.exists(target_folder.name):
        logger.info("Creating folder %s", target_folder.name)
        mailbox.folder.create(target_folder.name)

    move_results = mailbox.move(
        [i.text() for i in matches], target_folder.name
    )  # type: Any

    if move_results:
        flat = flatten(move_results)
        ids = filter(lambda i: i is not None and i != "OK", flat)

        logger.info(
            "Moved %d message(s) from %s to %s.",
            len(list(ids)),
            source_folder.name,
            target_folder.name,
        )
    else:
        logger.info(
            "No messages found matching the pattern set: %s.",
            show_patterns,
        )


def gather_stats(mailbox: MailBox) -> List[FolderStats]:
    return [
        FolderStats(name=i, count=mailbox.folder.status(i)["MESSAGES"])
        for i in [j["name"] for j in mailbox.folder.list()]
    ]
