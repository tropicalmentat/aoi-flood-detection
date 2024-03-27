import sqlite3
import logging

logger = logging.getLogger(__name__)
DB_PATH=f'./data/source.db'

def init_database():

    sqlite3.connect(
        database=DB_PATH)

    return

if __name__=="__main__":
    init_database()
