from pathlib import Path

import pytest

from metadata_driver_aws.data_plugin import Plugin


@pytest.fixture
def aws_plugin():
    config_path = Path(__file__).parent / "resources/config.ini"
    return Plugin(config_path.as_posix())


@pytest.fixture
def test_file_path():
    test_file_path = Path(__file__).parent / "resources/test_file.md"
    return test_file_path.as_posix()
