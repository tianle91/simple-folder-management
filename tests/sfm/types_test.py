from sfm.types import parse_raw_managed_dirs
from tests import TEST_RAW_CONFIG
from tests.sfm import TEST_PARSED_MANAGED_DIRS


def test_parse_raw_managed_dirs():
    raw_managed_dirs = TEST_RAW_CONFIG['managed_dirs']
    result = parse_raw_managed_dirs(raw_managed_dirs=raw_managed_dirs)
    assert result == TEST_PARSED_MANAGED_DIRS
