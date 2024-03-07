import os
import logging
from extract import (
    extract_flood,
    extract_true_color
)

from sys import stdout


logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

sensor = os.environ.get("SENSOR")
input = os.environ.get("INPUT")
output = os.environ.get("OUTPUT")

def main():
    logger.debug(sensor)
    logger.debug(input)
    logger.debug(output)

    if sensor=="landsat8":
        extract_flood()
    elif sensor=="sentinel2":
        pass

    return

if __name__=="__main__":
    main()