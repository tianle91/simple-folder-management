import yaml

TEST_CONFIG_YAML_PATH = 'tests/test_config.yaml'

with open(TEST_CONFIG_YAML_PATH) as f:
    TEST_RAW_CONFIG = yaml.safe_load(f)
