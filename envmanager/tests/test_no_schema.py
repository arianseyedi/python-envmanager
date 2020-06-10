import pytest

from envmanager.decorators import env_loader
from envmanager.tests.data import envloader_config_minimum

config = envloader_config_minimum

"""
Tests use of dictionary schema:
    - Set, retrieve and clear string keys and assert string values (as-is)
    - Get and clear schema keys and assert schema dictated types and expected values
"""


@pytest.fixture
def env():
    @env_loader(config)
    def inner():
        from envmanager.core import Env
        return Env(config)

    return inner()


def test_set_value(env):
    env.set('my_key', 1234)
    res = env.int('my_key')
    assert res == 1234, "testing setting custom string my_key failed"
    assert env.clear('my_key') is True, "testing setting custom string when mode popped"
    # cannot retrieve anymore or throws an error


def test_get_string_key_1(env):
    res = env("custom_validation_1")
    assert res == "custom_validation_1", "test getting custom_validation_1 failed"


def test_get_and_set(env):
    res = env("custom_validation_2")
    assert res == "custom_validation_2", "test getting custom_validation_2 failed"
    res = env("custom_validation_1")
    assert res == "custom_validation_1", "test getting custom_validation_1 failed"
    env.set('abcdefg', 1)
    res = env("abcdefg")
    assert res == "1", "test getting custom key failed"
    assert env.clear('abcdefg') is True, "testing setting custom string when mode popped"
