import os
import logging

from sys import stdout

logger = logging.getLogger(__name__)

logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

def main():
    logger.info('Start')

    return

if __name__=="__main__":
    main()