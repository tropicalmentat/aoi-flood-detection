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
                    SELECT * FROM flood
                    WHERE sensor='{sensor}'
                    ORDER BY created_on DESC
                        """)
    
    # get path of extracted
    # flood geotiff
    data = res.fetchone()

    if type=='flood':

        if data==None:
            return None

        path = data[4]
        cnxn.close()

        return path
    elif type=='impact':
        res = cur.execute(f"""
                        SELECT * FROM impact
                        WHERE src_id=='{data[0]}'
                        ORDER BY created_on DESC
                            """)
    
        # get path of extracted
        # flood geotiff
        data = res.fetchone()

        if data==None:
            return None

        path = data[5]
        cnxn.close()

        return path
    elif type=='overlap':
        res = cur.execute(f"""
                        SELECT * FROM rc_overlap
                        WHERE src_id=='{data[0]}'
                        ORDER BY created_on DESC
                            """)
    
        # get path of extracted
        # flood geotiff
        data = res.fetchone()

        if data==None:
            return None

        path = data[6]
        cnxn.close()

        return path
    elif type=='povinc':
        res = cur.execute(f"""
                        SELECT * FROM rc_povinc
                        WHERE src_id=='{data[0]}'
                        ORDER BY created_on DESC
                            """)
    
        # get path of extracted
        # flood geotiff
        data = res.fetchone()

        if data==None:
            return None

        path = data[4]
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

@app.route("/reclass_pov_inc/<string:sensor>")
def get_latest_reclassed_poverty_incidence(sensor: str):

    path = fetch_img_path(type='povinc', sensor=sensor)

    if path==None:
        return make_response('Not found', 404)

    with open(file=path, mode='rb') as src:
        img_bin = src.read()

        return img_bin

@app.route("/reclass_overlap_analysis/<string:sensor>")
def get_latest_reclassed_overlap_analysis(sensor: str):

    path = fetch_img_path(type='overlap', sensor=sensor)

    if path==None:
        return make_response('Not found', 404)

    with open(file=path, mode='rb') as src:
        img_bin = src.read()

        return img_bin