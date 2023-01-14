from app import SimpleFolderManagement

sfm = SimpleFolderManagement(config_path='tests/test_config.yaml')


def test_parse_dump_dir():
    result = sfm.parse_dump_dir()
    assert set(result.keys()) == {'keyword_A', 'keyword_B', 'no_hits'}, result
