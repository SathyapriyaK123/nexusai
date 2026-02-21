import time
import logging
import functools
def setup_logger(name: str):
    logger= logging.getlogger(name)
    logger.setlevel(logging.INFO)
    if logger.handlers:
        return logger
        connsole = loggig.streamHandler()
        connsole.setlevel(logging.INFO)
         '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
         datefmt='%H:%M:%S'
         ))
         logger.addHandler(connsole)
         return logger
         def retry(max_attempts=3, delay=2.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
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
        elapsed = time.time() - start
        return result
    return wrapper