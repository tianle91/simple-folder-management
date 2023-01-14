from app import SimpleFolderManagement

sfm = SimpleFolderManagement(config_path='tests/test_config.yaml')


def test_parse_dump_dir():
    result = sfm.parse_dump_dir()
    assert set(result.keys()) == {'keyword_A', 'keyword_B', 'no_hits'}, result


def test_get_moves():
    result = sfm.get_moves()
    assert result['keyword_A'][1] == 'tests/example_directory/managed/group_A_name/keyword_A'
    assert result['keyword_B'][1] == 'tests/example_directory/managed/group_A_name/keyword_B'
    assert result['no_hits'][1] is None
