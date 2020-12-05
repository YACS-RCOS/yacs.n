import os

class Constants:
    """
    Global Constants:
        - cache times
        - special strings
        - other things you don't want to accidently mistype
    """
    HOUR_IN_SECONDS = 60 * 60
    DAY_IN_SECONDS = 24 * HOUR_IN_SECONDS
    DB_NAME = os.environ.get('DB_NAME', 'yacs')
    DB_USER = os.environ.get('DB_USER', None)
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', None)
    DB_PASS = os.environ.get('DB_PASS', None)