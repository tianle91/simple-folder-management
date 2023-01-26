import yaml

from sfm.types import Group, ManagedDir, parse_raw_managed_dirs

TEST_CONFIG_YAML_PATH = 'tests/test_config.yaml'

with open(TEST_CONFIG_YAML_PATH) as f:
    TEST_RAW_CONFIG = yaml.safe_load(f)

TEST_PARSED_MANAGED_DIRS = {
    'managed_dir_A': ManagedDir(
        base_dir='/work/tests/example_directory_a',
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
        base_dir='/work/tests/example_directory_b',
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
