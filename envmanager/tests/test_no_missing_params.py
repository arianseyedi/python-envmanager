from pytest import fail

from envmanager.decorators import env_loader
from envmanager.exceptions import EagerValidationError
from envmanager.tests.data import envloader_config_eager_no_missing_param_enumSchema, \
    envloader_config_eager_no_missing_param_dictSchema

"""
Tests eager validation
"""


def test_passes_enum_schema():
    config = envloader_config_eager_no_missing_param_enumSchema
    try:
        @env_loader(config)
        def inner():
            from envmanager.core import Env
            return Env(config)
    except EagerValidationError:
        fail('Expecting Eager Validation to pass but threw EagerValidationError')
    except Exception as e:
        fail(f'Expecting Eager Validation to pass but threw {e}')


def test_passes_dict_schema():
    config = envloader_config_eager_no_missing_param_dictSchema
    try:
        @env_loader(config)
        def inner():
            from envmanager.core import Env
            return Env(config)
    except EagerValidationError:
        fail('Expecting Eager Validation to pass but threw EagerValidationError')
    except Exception as e:
        fail(f'Expecting Eager Validation to pass but threw {e}')
