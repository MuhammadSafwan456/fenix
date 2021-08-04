def get_value(key):
    from config.project_config import config
    return config[key]


JWT_SECRET_KEY = get_value("JWT_SECRET_KEY")
FLASK_KEY_SORTING = get_value("FLASK_KEY_SORTING")
DB_HOST = get_value("DB_HOST")
DB_NAME = get_value("DB_NAME")
DB_PORT = get_value("DB_PORT")
TOKEN_EXPIRY_SECONDS = get_value("TOKEN_EXPIRY_SECONDS")

