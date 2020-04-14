import pytest

from envmanager.decorators import env_loader
from envmanager.tests.data import envloader_config_multifile

config = envloader_config_multifile


@pytest.fixture
def env():
    @env_loader(config)
    def inner():
        from envmanager.core import Env
        return Env(config)

    return inner


def test_set_value(env):
    env.set('my_key', [1234])
    res = env('my_key')
    assert res == '[1234]', "testing setting custom string my_key failed"
    assert env.clear('my_key') is True, "testing setting custom string when mode popped"
    # cannot retrieve anymore or throws an error


def test_get_item_1(env):
    res = env('item_1')
    assert res == 'item_1', "getting item_1 failed"


def test_get_item_2(env):
    res = env('item_2')
    assert res == 'item_2', "getting item_2 failed"


def test_get_item_3(env):
    res = env('item_3')
    assert res == 'item_3', "getting item_3 failed"


def test_get_item_4(env):
    res = env('item_4')
    assert res == 'item_4', "getting item_4 failed"
