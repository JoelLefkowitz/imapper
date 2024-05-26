#!/usr/bin/env python
import json
import logging
import os
from .parsers import parse_clients
from .senders import fetch_senders
from .sweeper import sweep_on_loop
from docopt import docopt
from inspect import cleandoc
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

logger = logging.getLogger()

cli = cleandoc(
    """
    Imapper: IMAP message sweeper.

    Usage:
    imapper (sweep|senders) PATH --log=<logfile>

    Options:
    -h --help   Show this screen.
    """
)


def main() -> None:
    args = docopt(cli)

    if args["--log"]:
        logfile = args["--log"]
    else:
        logfile = os.path.join("logs", "imapper.log")

    Path(os.path.dirname(logfile)).mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[TimedRotatingFileHandler(logfile, "h", 1)],
    )

    with open(args["PATH"], "r", encoding="utf8") as stream:
        clients = parse_clients(json.load(stream))

    if args["sweep"]:
        sweep_on_loop(clients)

    if args["senders"]:
        fetch_senders(clients)


if __name__ == "__main__":
    main()
