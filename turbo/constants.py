import os

LOG_FORMAT = (
    "%(asctime)s - %(levelname)s - %(name)s[%(lineno)s][%(threadName)s] - %(message)s"
)

LOG_LEVEL = "ERROR"
LOG_LEVEL = os.getenv("RI_LOGLEVEL", LOG_LEVEL).upper()

TRACE = os.getenv("RI_TRACE", False)

SSL = os.getenv("REN_VERIFY_SSL", True)

API_VERSION = os.getenv("REN_API_VERSION", 0)
VERSION = "dev"  # TODO: Fix versioning based on internal format

TIMEOUT = os.getenv("REN_TIMEOUT", 300)

REMOTE_ADDR = os.getenv("REN_REMOTE", "https://r.ren-isac.net") + "/api"

MAX_FIELD_SIZE = 30

# TODO: Create generic class to manage all colum formats
MEMBER_COLUMS = ["name", "created_at", "updated_at"]
USER_COLUMS = ["username", "created_at", "updated_at"]

TOKEN = os.getenv("REN_TOKEN", None)
