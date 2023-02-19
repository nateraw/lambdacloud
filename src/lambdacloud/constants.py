import os


ENDPOINT = "https://cloud.lambdalabs.com/api/v1/"
# default cache
default_home = os.path.join(os.path.expanduser("~"), ".cache")
lambda_cache_home = os.path.expanduser(
    os.getenv(
        "LAMBDA_HOME",
        os.path.join(os.getenv("XDG_CACHE_HOME", default_home), "lambda"),
    )
)
LAMBDA_TOKEN_PATH = os.path.join(lambda_cache_home, "token")
