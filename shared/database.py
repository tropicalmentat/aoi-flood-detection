import sqlite3
import logging
from sys import stdout

logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)
DB_PATH=f'./data/source.db'

def main():

    logger.debug(f'Initializing database in {DB_PATH}')

    cnxn = sqlite3.connect(
        database=DB_PATH)
    
    cur = cnxn.cursor()

    cur.execute("CREATE TABLE source(id,sensor,path,created_on)")

    return

if __name__=="__main__":
    main()
