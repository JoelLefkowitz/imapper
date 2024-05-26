from src.utils import (chunks, flatten, increment_dict, intervals,
                       normcase_email, show_lst)


def test_chunks() -> None:
    assert list(chunks([1, 2, 3, 4, 5], 3)) == [[1, 2, 3], [4, 5]]


def test_normcase_email() -> None:
    assert normcase_email("joellefkowitz@hotmail.com") == "joellefkowitz_hotmail"
    assert normcase_email("joel.lefkowitz@ecs.co.uk") == "joel_lefkowitz_ecs"


def test_flatten() -> None:
    assert flatten([]) == []
    assert flatten([1, 2, 3]) == [1, 2, 3]
    assert flatten([1, 2, [3]]) == [1, 2, 3]
    assert flatten([[1], 2, [3]]) == [1, 2, 3]
    assert flatten([[1, 2], [3]]) == [1, 2, 3]
    assert flatten([[1, [2]], [3]]) == [1, 2, 3]
    assert flatten([[1, [2]], [[3, [4]]]]) == [1, 2, 3, 4]
    assert flatten([[1, [2]], [[3, [], [], [[[]]]]], 4]) == [1, 2, 3, 4]

    assert flatten(((1, (2)), ((3, (4))))) == [1, 2, 3, 4]
    assert flatten(((1, (2)), ((3, (), (), ((())))), 4)) == [1, 2, 3, 4]


def test_show_lst() -> None:
    assert show_lst(["1", "2", "3"], " - ") == "[1 - 2 - 3]"


def test_increment_dict() -> None:
    dct = {"a": 1}

    increment_dict(dct, "a")
    assert dct == {"a": 2}

    increment_dict(dct, "b")
    assert dct == {"a": 2, "b": 1}


def test_intervals() -> None:
    assert list(intervals(1, 2, 3)) == [(1, 3), (3, 5), (5, 7)]
