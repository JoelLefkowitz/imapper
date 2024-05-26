from typing import Any, Dict, Iterator, List, Tuple, TypeVar, Union

T = TypeVar("T")


def chunks(lst: List[T], size: int) -> Iterator[List[T]]:
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def normcase_email(account: str) -> str:
    sections = account.split("@")
    return ("_".join(sections[0].split(".") + [sections[1].split(".")[0]])).lower()


def flatten(lst: Union[List[Any], Tuple[Any]]) -> List[Any]:
    if len(lst) == 0:
        return []

    if isinstance(lst[0], (list, tuple)):
        return flatten(list(lst[0])) + flatten(list(lst[1:]))

    return list(lst[:1]) + flatten(list(lst[1:]))


def show_lst(lst: List[str], delimiter: str = ", ") -> str:
    return "".join(["[", delimiter.join(lst), "]"])


def increment_dict(dct: Dict[T, int], k: T) -> None:
    if k in dct:
        dct[k] += 1
    else:
        dct[k] = 1


def intervals(start: int, width: int, count: int) -> Iterator[Tuple[int, int]]:
    for i in range(count):
        yield (start + i * width, start + (i + 1) * width)
