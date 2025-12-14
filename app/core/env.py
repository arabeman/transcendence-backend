from environs import env

env.read_env()

DATABASE_URL = env.str("DATABASE_URL")
DEBUG = env.bool("DEBUG")