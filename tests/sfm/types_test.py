from sfm.types import Group, ManagedDir, parse_raw_managed_dirs
from tests import TEST_RAW_CONFIG

TEST_PARSED_MANAGED_DIRS = {
    'managed_dir_A': ManagedDir(
        base_dir='tests/example_directory_a',
        groups={
            'group_A': Group(
                path='group_A_name',
                keywords=['keyword_A', 'keyword_B'],
            ),
            'group_C': Group(
                path='some_subdir/group_C',
                keywords=['keyword_C']
            ),
        }
    ),
    'managed_dir_B': ManagedDir(
        base_dir='tests/example_directory_b',
        groups={
            'group_A': Group(
                path='group_A_name',
                keywords=['keyword_A', 'keyword_B'],
            )
        }
    )
}


def test_parse_raw_managed_dirs():
    raw_managed_dirs = TEST_RAW_CONFIG['managed_dirs']
    result = parse_raw_managed_dirs(raw_managed_dirs=raw_managed_dirs)
    assert result == TEST_PARSED_MANAGED_DIRS
