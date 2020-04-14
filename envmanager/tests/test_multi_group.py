import pytest

from envmanager.decorators import env_loader
from envmanager.tests.data import envloader_config_from_dict_multiapp

config = envloader_config_from_dict_multiapp

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

    return inner


def test_set_value(env):
    env.set('my_key', 1234)
    res = env.int('my_key')
    assert res == 1234, "testing setting custom string my_key failed"
    assert env.clear('my_key') is True, "testing setting custom string when mode popped"
    # cannot retrieve anymore or throws an error


def test_get_same_key_from_group_1(env):
    with env.group('GROUP1'):
        res = env('duplicate_string')
        assert res == 'dups', "test get duplicate_string failed"
        assert env.clear('duplicate_string') is True, "test get when duplicate_string popped"
        # cannot retrieve anymore or throws an error


def test_get_same_key_from_group_2(env):
    with env.group('GROUP2'):
        res = env('duplicate_string')
        assert res == 'dups2', "test get duplicate_string failed"
        assert env.clear('duplicate_string') is True, "test get when duplicate_string popped"
        # cannot retrieve anymore or throws an error


def test_get_same_key_from_group_both(env):
    with env.group('GROUP2'):
        res = env('duplicate_string')
        assert res == 'dups2', "test get duplicate_string failed"
        assert env.clear('duplicate_string') is True, "test get when duplicate_string popped"
        # cannot retrieve anymore or throws an error
    with env.group('GROUP1'):
        res = env('duplicate_string')
        assert res == 'dups', "test get duplicate_string failed"
        assert env.clear('duplicate_string') is True, "test get when duplicate_string popped"
        # cannot retrieve anymore or throws an error


def test_get_prepended_keys_from_group_1(env):
    with env.group('GROUP1'):
        with env.prepend('zero'):
            res = env('one')
            assert res == 'one', "test get zero_one failed"
            assert env.clear('one') is True, "test get when zero_one popped"
            with env.prepend('one'):
                res = env('two')
                assert res == 'two', "test get zero_one failed"
                assert env.clear('two') is True, "testing setting when zero_one popped"
