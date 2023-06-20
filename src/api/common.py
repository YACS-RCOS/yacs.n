import hashlib
import bcrypt
import os

# def assert_keys_in_form_exist(form, keys):
#     """
#     Check all the keys exist in the form.
#     :param form: object form
#     :param keys: required keys
#     :return: True if all the keys exist. Otherwise return false.
#     """
#     if form is None:
#         return False

#     if type(form) is not dict:
#         return False

#     for key in keys:
#         if key not in form.keys():
#             return False

#     return True


# def encrypt(str):
#     """
#     Encrypt the string using SHA256
#     :param str: string to be encrypted
#     :return: SHA256 encrypted string
#     """
#     encrypt_str = hashlib.sha256(str.encode()).hexdigest()
#     return encrypt_str

def hash_password(password):
    """
    Hashes the password using bcrypt with a randomly generated salt
    :param password: the password to be hashed
    :return: the hashed password as bytes
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password

def verify_password(password, hashed_password):
    """
    Verifies the password against the provided hashed password
    :param password: the password to be verified
    :param hashed_password: the hashed password to be verified against
    :return: True if the password is valid, False otherwise
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
