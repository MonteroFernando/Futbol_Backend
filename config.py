from dotenv import dotenv_values

class Config:
    config= dotenv_values(".env")

    JWT_SECRET_KEY=config['JWT_SECRET_KEY']
    SERVER_NAME="127.0.0.1:5001"
    DEBUG=True

    DATABASE_USERNAME=config['DATABASE_USERNAME']
    DATABASE_PASSWORD=config['DATABASE_PASSWORD']
    DATABASE_HOST=config['DATABASE_HOST']
    DATABASE_PORT=config['DATABASE_PORT']

    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is missing from .env")
    