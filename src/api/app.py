import os
import logging
import sqlite3
from flask import Flask, make_response

logger = logging.getLogger(__name__)

app = Flask(__name__)

DB_PATH = './data/source.db'

if os.path.exists(path=DB_PATH):
    logger.info(f'Database exists!')
else:
    raise FileNotFoundError()

def fetch_img_path(type:str, sensor: str):
        
    try:
        usr_name = os.environ.get("USER")
        logger.debug(usr_name)
        cnxn = sqlite3.connect(database=DB_PATH)
    except sqlite3.OperationalError as e:
        # we handle this because the database
        # is created with root ownership
        import pwd
        import grp
        usr_name = os.environ.get("USER")
        uid = pwd.getpwnam(usr_name).pw_uid
        gid = grp.getgrnam(usr_name).gr_gid
        os.chown(path=DB_PATH,uid=uid,gid=gid)

    cur = cnxn.cursor()

    res = cur.execute(f"""
                    SELECT * FROM {type}
                    WHERE sensor='{sensor}'
                    ORDER BY created_on DESC
                        """)
    
    # get path of extracted
    # flood geotiff
    data = res.fetchone()

    if data==None:
        return None

    path = data[2]
    cnxn.close()

    return path

@app.route("/catalog")
def get_catalog():

    return

@app.route("/flood/<string:sensor>")
def get_latest_flood(sensor: str):

    path = fetch_img_path(type='flood', sensor=sensor)

    if path==None:
        return make_response('Not found', 404)

    with open(file=path, mode='rb') as src:
        img_bin = src.read()

        return img_bin

@app.route("/impact/<string:sensor>")
def get_latest_impact(sensor: str):

    path = fetch_img_path(type='impact', sensor=sensor)

    if path==None:
        return make_response('Not found', 404)

    with open(file=path, mode='rb') as src:
        img_bin = src.read()

        return img_bin