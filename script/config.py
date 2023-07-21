import os

POSTGRES_DB: str = os.environ.get('POSTGRES_DB')
POSTGRES_USER: str = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST: str = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT: str = os.environ.get('POSTGRES_PORT')

LENGTH_STRING: int = 30

STARTING_DATABASE: int = 20
QUERY_RETRY_TIME: int = 60

MAX_RECORDS: int = 30
