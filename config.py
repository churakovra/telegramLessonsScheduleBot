from dotenv import dotenv_values


class Config:
    TOKEN = dotenv_values().get('TOKEN')
    DB_PATH = dotenv_values().get('DB_PATH')
