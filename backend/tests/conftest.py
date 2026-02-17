import sys
from unittest.mock import MagicMock

# Mock pandas
sys.modules["pandas"] = MagicMock()

# Mock pydantic_settings
# We need a class for BaseSettings because config.py inherits from it
class MockBaseSettings:
    def __init__(self, **kwargs):
        pass

pydantic_settings_mock = MagicMock()
pydantic_settings_mock.BaseSettings = MockBaseSettings
sys.modules["pydantic_settings"] = pydantic_settings_mock

# Mock config
# We mock config to avoid loading the real config which depends on environment variables
# and potentially other missing dependencies.
config_mock = MagicMock()
settings_mock = MagicMock()
settings_mock.JSONL_DATA_PATH = "dummy_path"
# Add other settings if accessed by DataProcessor.__init__ or other methods
settings_mock.API_TITLE = "Test API"
config_mock.settings = settings_mock

sys.modules["config"] = config_mock
sys.modules["backend.config"] = config_mock
