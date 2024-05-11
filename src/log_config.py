import logging
import sys

logger = logging.getLogger('optica')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
log_format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

logger.addHandler(handler)