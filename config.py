import os


secret_key = os.environ.get("SECRET_KEY", "")
if len(secret_key) < 32 or not secret_key.strip():
    raise RuntimeError(
        "Set SECRET_KEY to a private random value of at least 32 characters "
        "before starting the application."
    )
