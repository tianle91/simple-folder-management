from typing import Dict, List, Tuple

import pytest

from app import get_moves
from sfm.types import Group


@pytest.mark.parametrize(
    ('path', 'groups', 'expected'),
    [
        pytest.param(
            'tests/example_directory_a',
            {'group_A': Group(
                path='group_A_name',
                keywords=['keyword_A'],
            )},
            [(
                'tests/example_directory_a/dump/keyword_A/',
                'tests/example_directory_a/group_A_name/keyword_A',
            )],
            id='single keyword single hit'
        ),
    ]
)
def test_get_moves(
    path: str,
    groups: Dict[str, Group],
    expected: List[Tuple[str, str]],
):
    result = get_moves(path=path, groups=groups)
    assert expected == result, result
