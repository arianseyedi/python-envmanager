import pytest

from envmanager.decorators import env_loader
from envmanager.tests.data import envloader_config_modes_and_common_section

config = envloader_config_modes_and_common_section

"""
Tests eager validation
"""


@pytest.fixture
def env():
    @env_loader(config)
    def inner():
        from envmanager.core import Env
        return Env(config)

    return inner


def test_set_value(env):
    env.set('my_key', 1234)
    res = env.int('my_key')
    assert res == 1234, "testing setting custom string my_key failed"
    assert env.clear('my_key') is True, "expecting True when mode popped"
    # cannot retrieve anymore or throws an error


def test_get_correct_environment_var(env):
    res = env('myenvironment')
    assert res == 'prod', "value-check of the enrivonment failed"


def test_get_value_from_common_section(env):
    res = env('common_value')
    assert res == 'common_value', "getting common value from common section failed"


def test_get_value_from_correct_environment(env):
    res = env('value')
    assert res == 'prod', "getting environment-depepndent value from configured common section failed"
