import logging
import sys


logger = logging.getLogger("bolivia_data_collector")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s", datefmt="%H:%M:%S")
handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(handler)
