from enum import Enum

from marshmallow import fields
from marshmallow.validate import OneOf

from envmanager.core import Validator


class ComplexValidator(Validator):
    def __init__(self, val):
        self.val = val

    def validate(self, value):
        if value != self.val:
            raise Exception('failed validation', value)
        return value


dict_schema = {
    'mode': fields.Str(validate=OneOf(['prod', 'dev', 'staging', 'local'])),  # accepts any marshmallow field,
    'custom_validation_1': ComplexValidator('custom_validation_1'),
    'custom_validation_2': ComplexValidator('custom_validation_2'),
    'str_validation_abcd': str,
    'str_validation_1234': str,
    'int_validation_1': int,
    'int_validation_minus_1': int,
    'email_marshmallow_bytectgroup_at_gmail_dot_com': fields.Email(),
    'email_marshmallow_a_dot_b_at_gmail_dot_com': fields.Email(),
}


class GroupTwoSchema(Enum):
    mode = fields.Str(validate=OneOf(['prod', 'dev', 'staging', 'local']))  # accepts any marshmallow field
    custom_validation_3 = ComplexValidator('custom_validation_3')
    custom_validation_4 = ComplexValidator('custom_validation_4')
    str_validation_jjjj = fields.Str()
    str_validation_7777 = fields.Str()
    int_validation_3 = fields.Int()
    int_validation_minus_3 = fields.Int()
    email_marshmallow_bytectltd_at_gmail_dot_com = fields.Email()
    email_marshmallow_k_dot_y_at_gmail_dot_com = fields.Email()


class GroupOneSchema(Enum):
    mode = fields.Str(validate=OneOf(['prod', 'dev', 'staging', 'local']))  # accepts any marshmallow field
    custom_validation_1 = ComplexValidator('custom_validation_1')
    custom_validation_2 = ComplexValidator('custom_validation_2')
    str_validation_abcd = fields.Str()
    str_validation_1234 = fields.Str()
    int_validation_1 = fields.Int()
    int_validation_minus_1 = fields.Int()
    email_marshmallow_bytectgroup_at_gmail_dot_com = fields.Email()
    email_marshmallow_a_dot_b_at_gmail_dot_com = fields.Email()


class EagerSchema(Enum):
    validation_error_email_marshmallow = fields.Email()
    validation_error_custom = ComplexValidator('this one will not be validated.')
    validation_error_int = int


class EagerSchemaWithExtraParam(Enum):
    not_in_the_list = int
