from pytest import fail

from envmanager.decorators import env_loader
from envmanager.exceptions import EagerValidationError
from envmanager.tests.data import envloader_config_eager_missing_param_enumSchema, \
    envloader_config_eager_missing_param_dictSchema

"""
Tests eager validation
"""


def test_throws_validation_error_missing_param_enum():
    config = envloader_config_eager_missing_param_enumSchema
    try:
        @env_loader(config)
        def inner():
            from envmanager.core import Env
            return Env(config)
    except EagerValidationError:
        pass
    except:
        fail('Expecting Eager Validation Error to be thrown, got nothing')


def test_throws_validation_error_missing_param_dict():
    config = envloader_config_eager_missing_param_dictSchema
    try:
        @env_loader(config)
        def inner():
            from envmanager.core import Env
            return Env(config)
    except EagerValidationError:
        pass
    except:
        fail('Expecting Eager Validation Error to be thrown, got nothing')
