import pytest

from envmanager.decorators import env_loader
from envmanager.tests.data import envloader_config_enum
from envmanager.tests.resources import GroupOneSchema

config = envloader_config_enum

"""
Tests use of enum schema:
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


def test_mode(env):
    val = env(GroupOneSchema.mode)
    assert val == 'dev', "testing mode failed"
    assert env.clear(GroupOneSchema.mode) is True, "expecting true when mode popped"
    # cannot retrieve anymore or throws an error


def test_custom_validator_1(env):
    val = env(GroupOneSchema.custom_validation_1)
    assert val == 'custom_validation_1', "testing custom_validation_1 failed"
    assert env.clear(GroupOneSchema.custom_validation_1) is True, "expecting true when custom_validation_1 popped"
    # cannot retrieve anymore or throws an error


def test_custom_validator_2(env):
    val = env(GroupOneSchema.custom_validation_2)
    assert val == 'custom_validation_2', "testing custom_validation_2 failed"
    assert env.clear(GroupOneSchema.custom_validation_2) is True, "expecting true when custom_validation_2 popped"
    # cannot retrieve anymore or throws an error


def test_str_validation_abcd(env):
    val = env(GroupOneSchema.str_validation_abcd)
    assert val == 'abcd', "testing str_validation_abcd failed"
    assert env.clear(GroupOneSchema.str_validation_abcd) is True, "expecting true when str_validation_abcd popped"
    # cannot retrieve anymore or throws an error


def test_str_validation_1234(env):
    val = env(GroupOneSchema.str_validation_1234)
    assert val == '1234', "testing str_validation_1234 failed"
    assert env.clear(GroupOneSchema.str_validation_1234) is True, "expecting true when str_validation_1234 popped"
    # cannot retrieve anymore or throws an error


def test_int_validation_1(env):
    val = env(GroupOneSchema.int_validation_1)
    assert val == 1, "testing int_validation_1 failed"
    assert env.clear(GroupOneSchema.int_validation_1) is True, "expecting true when int_validation_1 popped"
    # cannot retrieve anymore or throws an error


def test_int_validation_minus_1(env):
    val = env(GroupOneSchema.int_validation_minus_1)
    assert val == -1, "testing int_validation_minus_1 failed"
    assert env.clear(GroupOneSchema.int_validation_minus_1) is True, "expecting true when int_validation_minus_1 popped"
    # cannot retrieve anymore or throws an error


def test_email_marshmallow_bytectgroup_at_gmail_dot_com(env):
    val = env(GroupOneSchema.email_marshmallow_bytectgroup_at_gmail_dot_com)
    assert val == 'bytectgroup@gmail.com', "testing test_email_marshmallow_bytectgroup_at_gmail_dot_com failed"
    assert env.clear(
        GroupOneSchema.email_marshmallow_bytectgroup_at_gmail_dot_com
    ) is True, "expecting true when email_marshmallow_bytectgroup_at_gmail_dot_com popped"
    # cannot retrieve anymore or throws an error


def test_email_marshmallow_a_dot_b_at_gmail_dot_com(env):
    val = env(GroupOneSchema.email_marshmallow_a_dot_b_at_gmail_dot_com)
    assert val == 'a.b@gmail.com', "testing test_email_marshmallow_a_dot_b_at_gmail_dot_com failed"
    assert env.clear(
        GroupOneSchema.email_marshmallow_a_dot_b_at_gmail_dot_com
    ) is True, "expecting true when email_marshmallow_a_dot_b_at_gmail_dot_com popped"
    # cannot retrieve anymore or throws an error


def test_set_value_2(env):
    env.set('my_key', '1234')
    res = env('my_key')
    assert res == '1234', "testing setting custom string my_key failed"
    assert env.clear('my_key') is True, "testing setting custom string when my_key popped"
    # cannot retrieve anymore or throws an error


def test_set_value_3(env):
    env.set('my_key_2', '2020-10-10')
    res = env('my_key_2')
    assert res == '2020-10-10', "testing setting custom string my_key_2  failed"
    assert env.clear('my_key_2') is True, "testing setting custom string when my_key_2 popped"
    # cannot retrieve anymore or throws an error


def test_get_unparsed_value(env):
    res = env('unparsed_str_klkl')
    assert res == 'klkl', "testing setting custom string unparsed_str_klkl  failed"
    assert env.clear('unparsed_str_klkl') is True, "testing setting custom string when unparsed_str_klkl popped"
    # cannot retrieve anymore or throws an error


def test_get_unparsed_value_2(env):
    res = env('unparsed_str_10')
    assert res == '10', "testing setting custom string unparsed_str_10  failed"
    assert env.clear('unparsed_str_10') is True, "testing setting custom string when unparsed_str_10 popped"
    # cannot retrieve anymore or throws an error
