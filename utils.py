import time
import logging
import functools

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return logger
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(
        '%(asctime)s | %(name)s | %(message)s',
        datefmt='%H:%M:%S'
    ))
    logger.addHandler(console)
    return logger

def retry(max_attempts=3, delay=2.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        raise
                    time.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator

def safe_parse_json(text, fallback=None):
    import json
    if fallback is None:
        fallback = {}
    try:
        cleaned = text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0]
        return json.loads(cleaned.strip())
    except:
        return fallback

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        return result
    return wrapper