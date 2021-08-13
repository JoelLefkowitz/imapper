from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Client:
    mailbox: str
    account: str
    folders: List[Folder]


@dataclass
class Folder:
    name: str
    patterns: List[str]


@dataclass
class FolderStats:
    name: str
    count: int
