import logging

def setup_logger():
    logger = logging.getLogger("BotDesk")
    handler = logging.FileHandler("botdesk.log")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger