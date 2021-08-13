import json
import logging
from inspect import cleandoc
from logging.handlers import TimedRotatingFileHandler

from docopt import docopt

from .parsers import parse_clients
from .senders import fetch_senders
from .sweeper import sweep_on_loop

logger = logging.getLogger()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[TimedRotatingFileHandler("imapper.log", "h", 1)],
)

cli = cleandoc(
    """
    Imapper: IMAP message sweeper.

    Usage:
    imapper (sweep|senders) PATH

    Options:
    -h --help     Show this screen.
    """
)


def main() -> None:
    args = docopt(cli)

    with open(args["PATH"]) as stream:
        clients = parse_clients(json.load(stream))

    if args["sweep"]:
        sweep_on_loop(clients)

    if args["senders"]:
        fetch_senders(clients)


if __name__ == "__main__":
    main()
