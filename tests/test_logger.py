import logging

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler_file = logging.FileHandler("test_log.log", mode='a', encoding='utf-8')
handler_file.setFormatter(formatter)

logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler_file)

logger.info("test message")
print("done")
