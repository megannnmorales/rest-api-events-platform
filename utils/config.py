import os

def get_secret(key_name, default=None):
    value = os.environ.get(key_name, default)
    if value is None:
        raise ValueError(f"Secret or enviroment variable '{key_name}' not found.")
    return value