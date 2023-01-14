from app import SimpleFolderManagement

sfm = SimpleFolderManagement(config_path='tests/test_config.yaml')


def test_parse_dump_dir():
    result = sfm.parse_dump_dir()
    assert set(result.keys()) == {'keyword_A', 'keyword_B', 'keyword_C', 'no_hits'}, result


def test_get_moves():
    result = sfm.get_moves()
    expected = {
        'keyword_A': (
            'tests/example_directory/dump/keyword_A/',
            'tests/example_directory/group_A_name/keyword_A'
        ),
        'keyword_B': (
            'tests/example_directory/dump/keyword_B/',
            'tests/example_directory/group_A_name/keyword_B'
        ),
        'keyword_C': (
            'tests/example_directory/dump/keyword_C/',
            'tests/example_directory/some_subdir/group_C/keyword_C'
        ),
        'no_hits': ('tests/example_directory/dump/no_hits/', None),
    }
    assert result == expected
