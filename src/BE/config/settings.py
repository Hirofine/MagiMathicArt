from decouple import config

class Settings:
    database_url = config('DATABASE_URL')
    secret_key = config('SECRET_KEY')
