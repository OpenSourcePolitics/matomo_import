import urllib3
import sqlite3
import os
import yaml


def init(config_file='config.yml'):
    global http, config, env, connection
    http = set_http_manager()
    config = set_config(config_file)
    env = set_env_variables()
    connection = set_database_connection()


def set_http_manager():
    return urllib3.PoolManager()


def set_config(config_file):
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    try:
        (
            config['base_url_parameters'], config['requests']
        )
    except KeyError:
        raise KeyError("Config file wrongly set")

    return config


def set_env_variables():
    env = {
        'base_url': os.getenv('BASE_URL'),
        'db_name' : os.getenv('DB_NAME'),
        'id_site' : os.getenv('ID_SITE'),
        'start_date': os.getenv('START_DATE'),
        'token_auth': os.getenv('TOKEN_AUTH')
    }

    if None in env.values():
        raise KeyError(
            f"One or multiple environment variables aren't set \n"
            f"Environment variables : {env}"
        )

    return env

def set_database_connection():
    connection = sqlite3.connect(os.environ['DB_NAME'])

    return connection
