import json
import logging
import os
from datetime import datetime, timedelta
from decimal import Decimal
from queue import LifoQueue
from typing import Callable
from urllib.parse import urlparse
from uuid import UUID

from envmanager.exceptions import UnknownGroup
from envmanager.utils import is_primitive, env_get, make_key, validate_marshmallow_type, is_marshmallow, parse_custom, \
    join_prependers, get_raw_key, get_key_string_value, get_scheme_value, get_environ_keys_all, env_pop, \
    get_value_of_prepended_word, build_plans, read_plan_and_load_environs_for_apps, ReservableEnvSections, \
    ReservableEnvKeys


class EnvManagerConfig:
    def __init__(self, env_paths=None,
                 group_name="PYTHON_APPLICATION",
                 eager_validate=False,
                 environment_mode=None,
                 schema=None,
                 common_section_identifier=ReservableEnvSections.common.value,
                 environment_identifier_key=ReservableEnvKeys.environment_mode.value,
                 plan=None):
        """
        Configuration settings as a plain python object
        :param group_name: name of the application which is to be configured
        :param eager_validate:
        :param schema:
        :param common_section_identifier: the string value of the section common to all environments
        :param environment_identifier_key:
        """
        if plan is not None:
            self.plan = plan
        elif env_paths is None:
            raise ValueError('Path to environment variable must be provided')
        else:
            self.plan = build_plans(group_name=group_name,
                                    env_paths=env_paths,
                                    schema=schema,
                                    environment_mode=environment_mode,
                                    eager_validate=eager_validate,
                                    common_section_identifier=common_section_identifier,
                                    environment_identifier_key=environment_identifier_key)

    @staticmethod
    def by_group(dict_object: dict, environment_mode=None):
        plans = {}
        for group_name, settings in dict_object.items():
            plans.update(build_plans(group_name=group_name,
                                     env_paths=settings['env_paths'],
                                     schema=settings.get('schema'),
                                     environment_mode=environment_mode,
                                     eager_validate=settings.get('eager_validate'),
                                     common_section_identifier=settings.get('common_section_identifier'),
                                     environment_identifier_key=settings.get('environment_identifier_key')))
        return EnvManagerConfig(plan=plans)


class Env:
    def __init__(self, config: EnvManagerConfig):
        """
        :param config:
        """
        self.__config = config
        self.__prepend_word_queue = LifoQueue(10)  # maximum 10 nested contexts
        self.__prepend_word = None  # will be unset for multi-app
        self.__group_name = None
        if isinstance(config, EnvManagerConfig):  # i.e. no need for context management
            self.__group_name = list(config.plan.keys())[0]

    def prepend(self, name):
        """
        Used in a context call to obtain keys prepended by a certain word for a known group (group must be known before
        calling object in a context)
        :param name:
        :return:
        """
        self.__prepend_word_queue.put(name)
        if self.__prepend_word is not None:
            self.__prepend_word = join_prependers(self.__prepend_word, name)
        else:
            self.__prepend_word = name
        return self

    def group(self, name):
        """
        Used in a context call to set group declared in the configuration
        :param name: name of the group
        :return:
        """
        self.__group_name = name
        return self

    def __enter__(self):
        """
        context entry
        :return:
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        context exit
        :param exc_type:
        :param exc_value:
        :param exc_traceback:
        :return:
        """
        if self.__prepend_word_queue.empty():
            self.__prepend_word = None
        else:
            item = self.__prepend_word_queue.get()
            word_length_pls_underscore = len(item) + 1 if not self.__prepend_word_queue.empty() else len(item)
            self.__prepend_word = get_value_of_prepended_word(self.__prepend_word, word_length_pls_underscore)

    def __call__(self, key, parser=None):
        """
        env getter
        :param key: target environment variable
        :param parser: parser function. Overrides the schema. When missing, the original schema is used if exits.
            In case of no parsing schema or parser, the value is returned as obtained from the source.
        :return:
        """
        if self.__group_name is None:
            raise UnknownGroup
        key_set = self.__config.plan.get(self.__group_name).get('schema')  # enum or dict
        if key_set is not None and parser is None:
            _key = get_key_string_value(key, key_set)
            val = env_get(get_raw_key(self.__prepend_word, _key), self.__group_name)
            _scheme = get_scheme_value(_key, key_set)
            if _scheme is not None:
                if is_primitive(_scheme):
                    res = _scheme(val)
                    return res
                elif is_marshmallow(_scheme):
                    res = validate_marshmallow_type(_key, _scheme, val)
                    return res
                res = _scheme.validate(val)
                return res
            else:
                return self.__get_maybe_parsed_key(key, parser)
        else:
            return self.__get_maybe_parsed_key(key, parser)

    def keys(self):
        """

        :return:
        """
        return get_environ_keys_all(list(self.__config.plan.keys()))

    def clear(self, key: str):
        """

        :param key: target environment variable
        :return: true if successful, false if not
        """
        if self.__group_name is None:
            raise UnknownGroup
        key_set = self.__config.plan.get(self.__group_name).get('schema')  # enum or dict
        _key = get_key_string_value(key, key_set)
        try:
            res = env_pop(get_raw_key(self.__prepend_word, _key), self.__group_name)
            return res is not None
        except:
            return False

    def set(self, key, value):
        """

        :param key: target environment variable
        :param value:
        :return:
        """
        raw_key = get_raw_key(self.__prepend_word, key)
        environ_key = make_key(self.__group_name, raw_key)
        os.environ[environ_key] = str(value)

    def str(self, key):
        """
        parses the target environment variable as a string
        :param key: target environment variable
        :return: float object
        """
        return self(key, parser=lambda x: str(x))

    def bool(self, key):
        """
        parses the target environment variable as a string
        :param key: target environment variable
        :return: float object
        """
        return self(key, parser=lambda x: bool(x))

    def int(self, key):
        """
        parses the target environment variable as a string
        :param key: target environment variable
        :return: target as int
        """
        return self(key, parser=lambda x: int(x))

    def float(self, key):
        """
        parses the target environment variable as a float
        :param key: target environment variable
        :return: float object
        """
        return self(key, parser=lambda x: float(x))

    def dict(self, key):
        """
        parses the target environment variable as a dictionary using json.loads function
        :param key: target environment variable
        :return: target as dictionary
        """
        return self(key, parser=lambda x: json.loads(x))

    def decimal(self, key, context=None):
        """
        parses the target environment variable as a Decimal object
        :param key: target environment variable
        :param context: Decimal object context keyword argument. Default is None
        :return: Decimal object
        """
        return self(key, parser=lambda x: Decimal(x, context=context))

    def list(self, key):
        """
        parses the target environment variable as a string
        :param key: target environment variable
        :return: target as list
        """
        return self(key, parser=lambda x: json.loads(x))

    def json(self, key, **loads_kwargs):
        """
        parses the target environment variable as a json using json.loads and then json.dumps functions
        :param key: target environment variable
        :param loads_kwargs: the json.loads function keyword arguments
        :return: target as json
        """
        return self(key, parser=lambda x: json.dumps(json.loads(x, **loads_kwargs)))

    def datetime(self, key, date_format='%m/%d/%y %H:%M:%S'):
        """
        parses the target environment variable as a datetime object:
            datetime_str = '09/19/18 13:55:26'
            datetime_object = datetime.strptime(datetime_str, '%m/%d/%y %H:%M:%S')
        :param key: target environment variable
        :param date_format: target environment variable
        :return: datetime object
        """
        return self(key, parser=lambda x: datetime.strptime(x, date_format))

    def date(self, key, date_format='%m-%d-%Y'):
        """
        parses the target environment variable as a date object:
            date_str = '09-19-2018'
            date_object = datetime.strptime(date_str, '%m-%d-%Y').date()
        :param key: target environment variable
        :param date_format: target environment variable
        :return: date object
        """
        return self(key, parser=lambda x: datetime.strptime(x, date_format).date())

    def timedelta_sec(self, key):
        """
        parses the target environment variable as a timedelta in seconds
        :param key: target environment variable
        :return: timedelta object
        """
        return self(key, parser=lambda x: timedelta(seconds=x))

    def url(self, key):
        """
        parses the target environment variable as a url object
        constructs a url object using the urlparse method from urllib library.
        :param key: target environment variable
        :return: url object
        """
        return self(key, parser=lambda x: urlparse(x))

    def uuid(self, key, *args, **kwargs):
        """
        constructs a new UUID instance
        :param key: target environment variable
        :param args: UUID class args
        :param kwargs: UUID class kwargs
        :return: UUID object
        """
        return self(key, parser=lambda x: UUID(x, *args, **kwargs))

    def log_level_as_int(self, key):
        """
        converts the target environment variable to a valid log level as an integer using logging.getLevelName function
            e.g. parsing "DEBUG" will return integer value 10
        :param key: target environment variable
        :return: integer corresponding to the string log level
        """
        return self(key, parser=lambda x: logging.getLevelName(x))

    def log_level_as_str(self, key):
        """
        converts the target environment variable to a valid log level string value using logging.getLevelName function
            e.g. parsing 10 will return string value DEBUG
        :param key: target environment variable
        :return: integer corresponding to the string log level
        """
        return self(key, parser=lambda x: logging.getLevelName(int(x)))

    def custom_parse(self, key, parser_function: Callable):
        """
        parse using custom provided function. The function must take exactly 1 argument and parses the target variable
        passed to it as a string
        :param key: target environment variable
        :param parser_function:  custom provided function. The function must take exactly 1 argument and parses the target variable
        :return: same output expected from the parser funcion
        """
        return self(key, parser_function)

    def __get_maybe_parsed_key(self, key, parser):
        res = env_get(get_raw_key(self.__prepend_word, key), self.__group_name)
        parsed = parse_custom(res, parser)
        return parsed


def load_env(config_object: object):
    """
    Decorator function that runs pre-configurations before the main application is run
    @rtype: object
    """
    read_plan_and_load_environs_for_apps(config_object)


class Validator:
    """
    Validator interface
    """

    def validate(self, value):
        raise NotImplementedError
