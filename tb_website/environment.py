import os
import json
import base64

__all__ = ['BASE_DIR', 'absolute_path', 'get_int', 'get_bool', 'get_str', 'get_list', 'get_dict']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def get_int(name, default=0, required=False):
    """
    Get a numeric value from environment and convert it accordingly.
    Return default if value does not exist or fails to parse.
    """
    if name not in os.environ:
        if required:
            raise SystemError('ENV: Required parameter {} could not be found'.format(name))
        else:
            print('ENV ERROR: Nothing found for: {}'.format(name))
            return default

    try:
        value = os.environ.get(name, default)
        return int(value)
    except ValueError:
        if required:
            raise SystemError('ENV: Required parameter {} could not be parsed'.format(name))
        else:
            print('ENV ERROR: Non-numeric type found for: {}'.format(name))
            return default


def absolute_path(*args):  # noqa
    return os.path.join(BASE_DIR, *args)


def get_bool(name, default=False, required=False):  # noqa
    """
    Get a boolean value from environment variable.
    If the environment variable is not set or value is not one or "true" or
    "false", the default value is returned instead.
    """

    if name not in os.environ:
        if required:
            raise SystemError('ENV: Required parameter {} could not be found'.format(name))
        else:
            return default
    if os.environ[name].lower() in ['true', 'yes', '1', 'y']:
        return True
    elif os.environ[name].lower() in ['false', 'no', '0', 'n']:
        return False
    else:
        if required:
            raise SystemError('ENV: Required parameter {} could not be found'.format(name))
        else:
            return default


def get_str(name, default=None, required=False):  # noqa
    """
    Get a string value from environment variable.
    If the environment variable is not set, the default value is returned
    instead.
    """

    value = os.environ.get(name, default)
    if value is None:
        if required:
            raise SystemError('ENV: Required parameter {} could not be found'.format(name))
        else:
            print('ENV ERROR: Nothing found for: {}'.format(name))
            return default

    return value


def get_list(name, separator=',', default=None, required=False):  # noqa
    """
    Get a list of string values from environment variable.
    If the environment variable is not set, the default value is returned
    instead.
    """
    if name not in os.environ:
        if default is None:
            if required:
                raise SystemError('ENV: Required parameter {} could not be found'.format(name))
            else:
                print('ENV ERROR: Nothing found for: {}'.format(name))
                default = []
        return default
    return os.environ[name].split(separator)


def get_dict(name, b64=False, default=None, required=False):
    """
    Get JSON encoded string from environment variable and return
    the default if it does not exist.
    """
    if name not in os.environ:
        if default is None:
            if required:
                raise SystemError('ENV: Required parameter {} could not be found'.format(name))
            else:
                print('ENV ERROR: Nothing found for: {}'.format(name))
                default = {}
        return default
    try:
        # Check if encoded
        if b64:
            return json.loads(base64.b64decode(os.environ[name].encode()).decode())
        else:
            return json.loads(os.environ[name])

    except ValueError:
        if required:
            raise SystemError('ENV: Required parameter {} could not be decoded/parsed'.format(name=name))
        else:
            print('ENV ERROR: Failed to parse value for: {}'.format(name))
            return default
