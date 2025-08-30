
import logging
import sys
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def setup_logger(name: str = "poke_pipeline", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger

def make_session(total_retries: int = 3, backoff_factor: float = 0.3, status_forcelist=None) -> requests.Session:
    if status_forcelist is None:
        status_forcelist = [429, 500, 502, 503, 504]
    session = requests.Session()
    retries = Retry(
        total=total_retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
