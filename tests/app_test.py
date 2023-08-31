from typing import Dict, List, Tuple

import pytest

from app import get_folder_moves
from sfm.types import Group


@pytest.mark.parametrize(
    ("path", "groups", "expected"),
    [
        pytest.param(
            "tests/example_directory_a",
            {
                "group_A": Group(
                    path="group_A_name",
                    keywords=["keyword_A"],
                )
            },
            [
                (
                    "tests/example_directory_a/dump/keyword_A/",
                    "tests/example_directory_a/group_A_name/keyword_A",
                )
            ],
            id="single group, single keyword, single hit",
        ),
        pytest.param(
            "tests/example_directory_a",
            {
                "group_A": Group(
                    path="group_A_name",
                    keywords=["keyword_A", "keyword_B"],
                )
            },
            [
                (
                    "tests/example_directory_a/dump/keyword_A/",
                    "tests/example_directory_a/group_A_name/keyword_A",
                ),
                (
                    "tests/example_directory_a/dump/keyword_B/",
                    "tests/example_directory_a/group_A_name/keyword_B",
                ),
            ],
            id="single group, multiple keywords, multiple hits",
        ),
        pytest.param(
            "tests/example_directory_a",
            {
                "group_A": Group(
                    path="group_A_name",
                    keywords=["keyword_A", "keyword_B"],
                ),
                "group_C": Group(
                    path="some_subdir/group_C",
                    keywords=["keyword_C"],
                ),
            },
            [
                (
                    "tests/example_directory_a/dump/keyword_A/",
                    "tests/example_directory_a/group_A_name/keyword_A",
                ),
                (
                    "tests/example_directory_a/dump/keyword_B/",
                    "tests/example_directory_a/group_A_name/keyword_B",
                ),
                (
                    "tests/example_directory_a/dump/keyword_C/",
                    "tests/example_directory_a/some_subdir/group_C/keyword_C",
                ),
            ],
            id="multiple groups",
        ),
    ],
)
def test_get_moves(
    path: str,
    groups: Dict[str, Group],
    expected: List[Tuple[str, str]],
):
    result = get_folder_moves(path=path, groups=groups)
    assert sorted(expected) == sorted(result)
