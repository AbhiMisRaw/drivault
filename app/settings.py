import os

from dotenv import load_dotenv

load_dotenv()

# Get the database URL and convert postgresql:// to postgres:// for Tortoise ORM
db_url = os.getenv("POSTGRES_URL")


# Tortoise ORM expects 'postgres://' scheme, not 'postgresql://'
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgres://", 1)


TORTOISE_ORM = {
    "connections": {
        "default": db_url
    },
    "apps": {
        "models": [
            "app.models.user",
            "app.models.files",
            # "aerich.models"  # For migrations support
        ],
        "default_connection": "default"
    },
}