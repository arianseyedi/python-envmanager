from pytest import fail

from envmanager.decorators import env_loader
from envmanager.exceptions import EagerValidationError
from envmanager.tests.data import envloader_config_eager_primitive_error

config = envloader_config_eager_primitive_error

"""
Tests eager validation
"""


def test_throws_validation_error_int():
    try:
        @env_loader(config)
        def inner():
            from envmanager.core import Env
            return Env(config)
    except EagerValidationError:
        pass
    except:
        fail('Expecting Eager Validation Error to be thrown, got nothing')

def test_throws_validation_error_marshmallow():
    try:
        @env_loader(config)
        def inner():
            from envmanager.core import Env
            return Env(config)
    except EagerValidationError:
        pass
    except:
        fail('Expecting Eager Validation Error to be thrown, got nothing')


def test_throws_validation_error_custom():
    try:
        @env_loader(config)
        def inner():
            from envmanager.core import Env
            return Env(config)
    except EagerValidationError:
        pass
    except:
        fail('Expecting Eager Validation Error to be thrown, got nothing')