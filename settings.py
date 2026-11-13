"""
Settings for the end-to-end testing platform.
"""

import configparser
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

try:
    # Read configuration from the file
    confParser = configparser.ConfigParser(interpolation=None)
    file_path = os.path.join(BASE_DIR, 'settings.ini')
    confParser.read(file_path)

    # SECURITY WARNING: keep the secret key used in production secret!
    VOMS_PROXY_PASSWORD = confParser.get('common', 'VOMS_PROXY_PASSWORD')
    IRIS_CLIENT_ID = confParser.get('common', 'IRIS_CLIENT_ID')
    IRIS_CLIENT_SECRET = confParser.get('common', 'IRIS_CLIENT_SECRET')
    SKA_CLIENT_ID = confParser.get('common', 'SKA_CLIENT_ID')
    SKA_CLIENT_SECRET = confParser.get('common', 'SKA_CLIENT_SECRET')
    DB_HOST = confParser.get('common', 'DB_HOST')
    DB_USER = confParser.get('common', 'DB_USER')
    DB_PASSWORD = confParser.get('common', 'DB_PASSWORD')
    DB_DATABASE = confParser.get('common', 'DB_DATABASE')

except (configparser.NoSectionError) as err:
    print("Error in configuration file. Check that file exists first: %s" % err)
    sys.exit(1)
