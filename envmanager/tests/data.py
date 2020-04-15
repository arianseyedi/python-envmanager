import os

from envmanager.core import EnvManagerConfig
from envmanager.tests.resources import GroupTwoSchema, GroupOneSchema, dict_schema, EagerSchema, \
    EagerSchemaWithExtraParam, EagerSchemaNoMissingDict, EagerSchemaNoMissingEnum

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))  # Root directory of the project
ENVS_PATH = os.path.join(ROOT_DIR, 'envars_group_one.cfg')
ENVS_PATH_2 = os.path.join(ROOT_DIR, 'envars_group_two.cfg')
ENVS_PATH_CAST = os.path.join(ROOT_DIR, 'envars_casts.cfg')
ENVS_PATH_MULTIFILE_1 = os.path.join(ROOT_DIR, 'envars_multifile_1.cfg')
ENVS_PATH_MULTIFILE_2 = os.path.join(ROOT_DIR, 'envars_multifile_2.cfg')
ENVS_PATH_EAGER_PRIMITIVE = os.path.join(ROOT_DIR, 'envars_eager_primitive.cfg')
ENVS_PATH_EAGER_MARSHMALLOW = os.path.join(ROOT_DIR, 'envars_eager_marshmallow.cfg')
ENVS_PATH_EAGER_CUSTOM = os.path.join(ROOT_DIR, 'envars_eager_custom.cfg')
ENVS_PATH_EAGER_MODS_SINGLE = os.path.join(ROOT_DIR, 'envars_modes_single.cfg')
# ENVS_PATH_EAGER_MODS_MULTI = os.path.join(ROOT_DIR, 'envars_eager_custom.cfg')
ENVS_PATH_NO_MISSING = os.path.join(ROOT_DIR, 'envars_no_missing.cfg')

envloader_config_minimum = EnvManagerConfig(env_paths=[ENVS_PATH])

envloader_config_multifile = EnvManagerConfig(env_paths=[ENVS_PATH_MULTIFILE_1, ENVS_PATH_MULTIFILE_2])

envloader_config_enum = EnvManagerConfig(group_name='TESTERAPP', env_paths=[ENVS_PATH], schema=GroupOneSchema)

envloader_config_dict = EnvManagerConfig(group_name='TESTERAPP', env_paths=[ENVS_PATH], schema=dict_schema)

envloader_config_casts = EnvManagerConfig(group_name='TESTERAPP', env_paths=[ENVS_PATH_CAST])

envloader_config_eager_primitive_error = EnvManagerConfig(group_name='TESTERAPP',
                                                          env_paths=[ENVS_PATH_EAGER_PRIMITIVE],
                                                          schema=EagerSchema, eager_validate=True)
envloader_config_eager_marshmallow_error = EnvManagerConfig(group_name='TESTERAPP',
                                                            env_paths=[ENVS_PATH_EAGER_MARSHMALLOW], schema=EagerSchema,
                                                            eager_validate=True)
envloader_config_eager_custom_error = EnvManagerConfig(group_name='TESTERAPP',
                                                       env_paths=[ENVS_PATH_EAGER_CUSTOM],
                                                       schema=EagerSchema, eager_validate=True)

envloader_config_eager_missing_param_enumSchema = EnvManagerConfig(group_name='TESTERAPP',
                                                                   env_paths=[ENVS_PATH],
                                                                   schema=EagerSchemaWithExtraParam, eager_validate=True)

envloader_config_eager_missing_param_dictSchema = EnvManagerConfig(group_name='TESTERAPP',
                                                       env_paths=[ENVS_PATH],
                                                       schema={'missing_variable': str}, eager_validate=True)

envloader_config_eager_no_missing_param_enumSchema = EnvManagerConfig(group_name='TESTERAPP',
                                                                   env_paths=[ENVS_PATH_NO_MISSING],
                                                                   schema=EagerSchemaNoMissingEnum, eager_validate=True)

envloader_config_eager_no_missing_param_dictSchema = EnvManagerConfig(group_name='TESTERAPP',
                                                       env_paths=[ENVS_PATH_NO_MISSING],
                                                       schema=EagerSchemaNoMissingDict, eager_validate=True)

envloader_config_from_dict_multiapp = EnvManagerConfig.by_group({
    'GROUP1': {
        'env_paths': [ENVS_PATH],
        'schema': GroupOneSchema
    },
    'GROUP2': {
        'env_paths': [ENVS_PATH_2],
        'schema': GroupTwoSchema,
    }
})

envloader_config_modes_and_common_section = EnvManagerConfig(group_name='TESTERAPP',
                                                             env_paths=[ENVS_PATH_EAGER_MODS_SINGLE],
                                                             common_section_identifier='mysection',
                                                             # environment_identifier_key='myenvironment',
                                                             eager_validate=True)
