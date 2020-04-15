class UnknownGroup(Exception):
    """ Attribute not found. """

    def __init__(self, msg: str = None):
        if msg is not None:
            self.message = f'{msg}'
        else:
            self.message = 'Must specify the group prior to attempting to get the desird environment variable. ' \
                           'Use ".group(<group name>) method as context to configure the getter object."'

    def __str__(self):
        return self.message


class UnsupportedKeyType(Exception):
    """ Attribute not found. """

    def __init__(self, msg: str = None, key=None):
        if msg is not None:
            self.message = f'{msg}'
        else:
            self.message = f"The key {'of type ' + type(key) if key is not None else 'used'} is not supported. "

    def __str__(self):
        return self.message


class EagerValidationError(Exception):
    """ Attribute not found. """

    def __init__(self, msg: str = None, key=None, value=None, schema=None, missing_param=None):
        if msg is not None:
            self.message = f'{msg}'
        elif missing_param is not None:
            self.message = f'Key {missing_param} is present in the schema but missing.'
        else:
            expl = f'{key} with value {value} is not parsable to schema type {type(schema)}' if key is not None and schema is not None and value is not None else ''
            self.message = f"Eager Validation failed. Some environment variables have values that will not be " \
                           f"schema parsable: {expl}."

    def __str__(self):
        return self.message
