import os
from tempfile import TemporaryDirectory
from typing import Dict, List, Tuple

import pytest
import yaml

from app import get_folder_moves
from sfm.types import Group

TEST_DIRTREE_PATH = "tests/test_dirtree.yaml"


@pytest.mark.parametrize(
    ("groups", "expected"),
    [
        pytest.param(
            {
                "group_A": Group(
                    path="group_A_name",
                    keywords=["keyword_A"],
                )
            },
            [
                (
                    "dump/keyword_A/",
                    "group_A_name",
                )
            ],
            id="single group, single keyword, single hit",
        ),
        pytest.param(
            {
                "group_A": Group(
                    path="group_A_name",
                    keywords=["keyword_A", "keyword_B"],
                )
            },
            [
                (
                    "dump/keyword_A/",
                    "group_A_name",
                ),
                (
                    "dump/keyword_B/",
                    "group_A_name",
                ),
            ],
            id="single group, multiple keywords, multiple hits",
        ),
        pytest.param(
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
                    "dump/keyword_A/",
                    "group_A_name",
                ),
                (
                    "dump/keyword_B/",
                    "group_A_name",
                ),
                (
                    "dump/keyword_C/",
                    "some_subdir/group_C",
                ),
            ],
            id="multiple groups",
        ),
    ],
)
def test_get_moves(
    groups: Dict[str, Group],
    expected: List[Tuple[str, str]],
):
    with TemporaryDirectory() as tmpdir:
        with open(TEST_DIRTREE_PATH) as f:
            d = yaml.safe_load(f)
        make_test_dir(d=d, tmpdir=tmpdir)
        result = get_folder_moves(path=tmpdir, groups=groups)
        expected_full = [
            (
                os.path.join(tmpdir, from_relative_path),
                os.path.join(tmpdir, to_relative_path),
            )
            for from_relative_path, to_relative_path in expected
        ]
        assert sorted(expected_full) == sorted(result)


def make_test_dir(d: dict, tmpdir: str):
    for k, v in d.items():
        if k == "_files":
            for v in d["_files"]:
                with open(os.path.join(tmpdir, v), "w") as f:
                    f.write("")
        else:
            newtmpdir = os.path.join(tmpdir, k)
            # should be first time creating this directory
            os.makedirs(newtmpdir, exist_ok=False)
            make_test_dir(d=v, tmpdir=newtmpdir)
