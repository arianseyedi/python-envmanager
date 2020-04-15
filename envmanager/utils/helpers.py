import configparser
import os
from enum import Enum

from marshmallow import Schema

from envmanager.exceptions import UnsupportedKeyType, EagerValidationError
from envmanager.utils.resources import ReservableEnvSections, ReservableEnvKeys


def is_primitive(obj):
    return isinstance(obj, type)


def env_get(raw_key, prepender):
    return os.environ.get(make_key(prepender, raw_key))


def read_env_from_path(path):
    _config = configparser.ConfigParser()
    _config.read(path)
    return _config


def get_env_mode(_base_config, common_section_name, mode_key):
    try:
        return _base_config.get(common_section_name, mode_key)
    except:
        return None


def make_key(prepender, key):
    return f'{str(prepender).upper()}_{str(key)}'


def set_environ_var(parsed_cfg, section, k, ppw):
    key = make_key(ppw, k)
    os.environ[key] = parsed_cfg[section][k]


def setenv(parsed_cfg, prepender, mode=None, schema=None, common_section_name=None):
    """
    sets all available environment variables prepended by the app name, given a path
    :param mode: mode of environment. besides the common section, only the variables of the given mode
        (dev, local or prod) will be written
    :param parsed_cfg: parsed cfg object
    :return:
    """
    common_section = ReservableEnvSections.common.value if common_section_name is None else common_section_name
    for k in parsed_cfg[common_section]:
        validate_schema_eager(parsed_cfg, common_section, k, schema)
        set_environ_var(parsed_cfg, common_section, k, prepender)
    if mode and parsed_cfg.has_section(mode):
        for _k in parsed_cfg[mode]:
            validate_schema_eager(parsed_cfg, common_section, _k, schema)
            set_environ_var(parsed_cfg, mode, _k, prepender)


def load_envs(path, prepender, schema=None, mode=None, mode_key=None, common_section_name=None):
    parsed_cfg = read_env_from_path(path)
    mode = mode if mode is not None else get_env_mode(parsed_cfg, common_section_name=common_section_name,
                                                      mode_key=mode_key)
    setenv(parsed_cfg=parsed_cfg,
           mode=mode,
           prepender=prepender,
           schema=schema,
           common_section_name=common_section_name)


def validate_marshmallow_type(_key, _type, val):
    TheSchema = Schema.from_dict(
        {_key: _type}
    )
    res = TheSchema().load({_key: val})
    if res:
        return res[_key]


def is_marshmallow(_type):
    return 'marshmallow' in _type.__class__.__module__


def is_function(_type):
    return callable(_type)


def is_class_instance(_type):
    return isinstance(_type, object) and not isinstance(_type, dict)


def is_class(_type):
    return hasattr(_type, __dict__) and not isinstance(_type, dict)


def parse_custom(res, parser):
    if is_function(parser):
        return parser(res)
    return res


def join_prependers(pp1, pp2):
    return pp1 + '_' + pp2


def get_raw_key(prepend_word, key):
    if prepend_word is None:
        return key
    else:
        return join_prependers(prepend_word, key)


def get_key_string_value(key, schema):
    if type(key) == str:
        return key
    elif type(schema) is type(Enum):
        return key.name
    raise UnsupportedKeyType


def get_scheme_value(key, key_set):
    if type(key_set) is dict:
        dict_val = key_set.get(key)
        if dict_val is not None:
            return dict_val
    elif type(key_set) is type(Enum):
        enum_key = key_set.__dict__.get(key)
        if enum_key is not None:
            return enum_key.value


def get_environ_keys_all(param):
    all_unfiltered = os.environ.keys()
    filter_keys = lambda ls: ['_'.join([str(elem) for elem in i.split('_')[1:]]) for i in ls if
                              i.split('_')[0] in param]
    return filter_keys(all_unfiltered)


def env_pop(raw_key, prepender):
    return os.environ.pop(make_key(prepender, raw_key))


def get_value_of_prepended_word(latest, word_length_pls_underscore):
    return None if len(latest) == word_length_pls_underscore else latest[0: len(
        latest) - word_length_pls_underscore]


def load_for_app(app_name, env_paths, schema=None, common_section_name=None, mode=None, mode_key=None):
    for path in env_paths:
        load_envs(path=path,
                  prepender=app_name,
                  schema=schema,
                  mode=mode,
                  common_section_name=common_section_name,
                  mode_key=mode_key)  # Load Environment Variables


def build_plans(group_name, env_paths, schema, eager_validate,
                environment_mode,
                common_section_identifier=ReservableEnvSections.common.value,
                environment_identifier_key=ReservableEnvKeys.environment_mode.value):
    return {
        group_name: {
            'env_paths': env_paths,
            'schema': schema,
            'environment_mode': environment_mode,
            'eager_validate': eager_validate,
            'environment_identifier_key': environment_identifier_key,
            'common_section_identifier': common_section_identifier
        }
    }


def read_plan_and_load_environs_for_apps(config_object):
    apps_plan = getattr(config_object, 'plan')
    for app_name, config in apps_plan.items():
        schema = config.get('schema') if config.get('eager_validate') else None
        common_section_name = config.get('common_section_identifier') if config.get(
            'common_section_identifier') else None
        mode_key = config.get('environment_identifier_key') if config.get('environment_identifier_key') else None
        mode = config.get('mode') if config.get('mode') else None
        load_for_app(app_name=app_name,
                     env_paths=config['env_paths'],
                     schema=schema,
                     mode=mode,
                     common_section_name=common_section_name,
                     mode_key=mode_key)


def get_scheme_value_from_key_string_value(key, key_set):
    if type(key_set) is dict:
        dict_val = key_set.get(key)
        if dict_val is not None:
            return dict_val
        else:
            raise EagerValidationError(missing_param=key)
    elif type(key_set) is type(Enum):
        try:
            enum_key = getattr(key_set, key)
            if enum_key is not None:
                return enum_key.value
        except AttributeError:
            raise EagerValidationError(missing_param=key)


def validate_schema_eager(parsed_cfg, section, key, schema):
    key_set = schema  # enum or dict
    if key_set is not None:
        _scheme = get_scheme_value_from_key_string_value(key, key_set)
        val = parsed_cfg[section][key]
        if _scheme is not None:
            if is_primitive(_scheme):
                try:
                    _scheme(val)
                    return
                except:
                    raise EagerValidationError(key=key, value=val, schema=_scheme)
            elif is_marshmallow(_scheme):
                try:
                    validate_marshmallow_type(key, _scheme, val)
                    return
                except:
                    raise EagerValidationError(key=key, value=val, schema=_scheme)
            try:
                _scheme.validate(val)
                return
            except:
                raise EagerValidationError(key=key, value=val, schema=_scheme)
