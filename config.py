import os


class Config:
    DB_URL = os.environ.get("DB_URL")
    TEMPLATES_AUTO_RELOAD = True