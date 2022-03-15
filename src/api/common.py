import hashlib


def assert_keys_in_form_exist(form, keys):
    """
    Check all the keys exist in the form.
    :param form: object form
    :param keys: required keys
    :return: True if all the keys exist. Otherwise return false.
    """
    if form is None:
        return False

    if type(form) is not dict:
        return False

    for key in keys:
        if key not in form.keys():
            return False

    return True


def encrypt(str):
    """
    Encrypt the string using SHA256
    :param str: string to be encrypted
    :return: SHA256 encrypted string
    """
    encrypt_str = hashlib.sha256(str.encode()).hexdigest()
    return encrypt_str
