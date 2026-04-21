import os

def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} is not set in environment variables.")
    return value