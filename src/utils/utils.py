from datetime import datetime
import time

def get_timestamp() -> str:
    # Get the current timestamp in seconds since the epoch
    return time.time()

def log_timestamp(marker: str=None) -> None:
    # Log the current timestamp in seconds since the epoch
    if marker is None:
        print(get_timestamp(), flush=True)
    else:
        print(f"{marker} - {get_timestamp()}", flush=True)

def get_datetime() -> str:
    # Get the datetime up to the microsecond in YYYYMMDD_HHMMSSUUUUUU format
    return datetime.now().strftime("%Y%m%d_%H%M%S%f")

