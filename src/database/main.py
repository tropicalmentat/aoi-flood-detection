import logging

from shared.database import init_db
from sys import stdout

logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

def main():

    init_db()

    return

if __name__=="__main__":
    main()