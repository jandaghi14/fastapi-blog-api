import logging
import sys

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler(sys.stderr)
handler_file = logging.FileHandler("app_log.log", mode='a', encoding='utf-8')

handler.setFormatter(formatter)
handler_file.setFormatter(formatter)

logger = logging.getLogger("fastapi_blog_api")
logger.setLevel(logging.INFO)

if not logger.handlers:  # prevent duplicate handlers on reimport
    logger.addHandler(handler)
    logger.addHandler(handler_file)
