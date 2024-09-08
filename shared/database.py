import sqlite3
import logging

logger = logging.getLogger(__name__)
DB_PATH=f'./data/source.db'

def init_db():

    logger.debug(f'Initializing database in {DB_PATH}')

    cnxn = sqlite3.connect(
        database=DB_PATH)
    
    cur = cnxn.cursor()
    # create table for flood extracted images
    cur.execute("CREATE TABLE flood(id,sensor,event,location,path,created_on)")
    # create table for flood impact images
    cur.execute("CREATE TABLE impact(id,src_id,sensor,event,location,path,created_on)")
    # create table for reclassed overlap analysis images
    cur.execute("CREATE TABLE rc_overlap(id,src_id,sensor,event,location,bounds_src,path,created_on)")
    # create table for reclassed poverty incidence images
    cur.execute("CREATE TABLE rc_povinc(id,src_id,sensor,povinc_src,path,created_on)")
    res = cur.execute("SELECT * FROM sqlite_master")
    logger.debug(res.fetchone())

    return

if __name__=="__main__":
    init_db()
