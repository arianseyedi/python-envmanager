import json
import logging
from datetime import datetime
from decimal import Decimal
from urllib.parse import urlparse
from uuid import UUID

import pytest

from envmanager.decorators import env_loader
from envmanager.tests.data import envloader_config_casts

config = envloader_config_casts

"""
Tests castings
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


def test_cast_str(env):
    res = env.str('unparsed_str')
    assert res == '1234', "casting unparsed_str failed"
    assert env.clear('unparsed_str') is True, "expecting True when unparsed_str popped"
    # cannot retrieve anymore or throws an error


def test_cast_bool(env):
    res = env.bool('unparsed_bool')
    assert res is True, "casting unparsed_bool failed"
    assert env.clear('unparsed_bool') is True, "expecting True when unparsed_bool popped"
    # cannot retrieve anymore or throws an error


def test_cast_int(env):
    res = env.int('unparsed_int')
    assert res == -2, "casting unparsed_int failed"
    assert env.clear('unparsed_int') is True, "expecting True when unparsed_int popped"
    # cannot retrieve anymore or throws an error


def test_cast_list(env):
    res = env.list('unparsed_list')
    assert res == [1, 2, 3, 'string'], "casting unparsed_int failed"
    assert env.clear('unparsed_list') is True, "expecting True when unparsed_list popped"
    # cannot retrieve anymore or throws an error


def test_cast_datetime(env):
    res = env.datetime('unparsed_datetime')
    assert type(res) is type(
        datetime.strptime('09/19/18 13:55:26', '%m/%d/%y %H:%M:%S')), "casting unparsed_datetime failed"
    assert env.clear('unparsed_datetime') is True, "expecting True when unparsed_datetime popped"
    # cannot retrieve anymore or throws an error


def test_cast_date(env):
    res = env.date('unparsed_date')
    assert type(res) is type(
        datetime.strptime('09-19-2018', '%m-%d-%Y').date()), "casting unparsed_date failed"
    assert env.clear('unparsed_date') is True, "expecting True when unparsed_date popped"
    # cannot retrieve anymore or throws an error


def test_url(env):
    res = env.url('unparsed_url')
    assert res.hostname == urlparse('https://stackoverflow.com/questions/').hostname, "casting unparsed_url failed"
    assert env.clear('unparsed_url') is True, "expecting True when unparsed_url popped"
    # cannot retrieve anymore or throws an error


def test_uuid(env):
    res = env.uuid('unparsed_uuid')
    assert res == UUID('12345678-1234-5678-1234-567812345678'), "casting unparsed_uuid failed"
    assert env.clear('unparsed_uuid') is True, "expecting True when unparsed_uuid popped"
    # cannot retrieve anymore or throws an error


def test_cast_log_level(env):
    res = env.log_level_as_int('unparsed_log')
    assert res == logging.getLevelName("DEBUG"), "casting unparsed_log failed"
    assert env.clear('unparsed_log') is True, "expecting True when unparsed_log popped"
    # cannot retrieve anymore or throws an error


def test_cast_log_level(env):
    res = env.log_level_as_str('unparsed_log_int')
    assert res == "DEBUG", "casting unparsed_log failed"
    assert env.clear('unparsed_log') is True, "expecting True when unparsed_log popped"
    # cannot retrieve anymore or throws an error


def test_cast_float(env):
    res = env.float('unparsed_float')
    assert res == 12345678.0, "casting unparsed_float failed"
    assert env.clear('unparsed_float') is True, "expecting True when unparsed_float popped"
    # cannot retrieve anymore or throws an error


def test_cast_dict(env):
    res = env.dict('unparsed_dict')
    assert res == {"a": 1}, "casting unparsed_dict failed"
    assert env.clear('unparsed_dict') is True, "expecting True when unparsed_dict popped"
    # cannot retrieve anymore or throws an error


def test_cast_decimal(env):
    res = env.decimal('unparsed_decimal')
    assert res == Decimal('12.2'), "casting unparsed_decimal failed"
    assert env.clear('unparsed_decimal') is True, "expecting True when  unparsed_decimal popped"
    # cannot retrieve anymore or throws an error


def test_cast_json(env):
    res = env.json('unparsed_json')
    assert res == json.dumps({"mmm": 12}), "casting unparsed_unparsed_json failed"
    assert env.clear('unparsed_json') is True, "expecting True when unparsed_unparsed_json popped"
    # cannot retrieve anymore or throws an error


def test_set_value_2(env):
    env.set('my_key', '1234')
    res = env('my_key')
    assert res == '1234', "testing setting custom string my_key failed"
    assert env.clear('my_key') is True, "expecting True when mode popped"
    # cannot retrieve anymore or throws an error


def test_set_value_3(env):
    env.set('my_key_2', '2020-10-10')
    res = env('my_key_2')
    assert res == '2020-10-10', "testing setting custom string my_key_2  failed"
    assert env.clear('my_key_2') is True, "expecting True when mode popped"
    # cannot retrieve anymore or throws an error
