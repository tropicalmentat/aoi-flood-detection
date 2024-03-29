import sqlite3
import logging
from sys import stdout

logger = logging.getLogger(__name__)
DB_PATH=f'./data/source.db'

def init_db():

    logger.debug(f'Initializing database in {DB_PATH}')

    cnxn = sqlite3.connect(
        database=DB_PATH)
    
    cur = cnxn.cursor()

    cur.execute("CREATE TABLE source(id,sensor,path,created_on)")

    res = cur.execute("SELECT * FROM sqlite_master")

    logger.debug(res.fetchone())

    return

if __name__=="__main__":
    init_db()
