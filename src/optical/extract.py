from shared.preprocess.landsat import radiance_to_reflectance
from rasterio.profiles import DefaultGTiffProfile
from uuid import uuid4

import os
import numpy.ma as ma
import shared.utils as utils
import logging
import rasterio as rio
import sqlite3
import datetime as dt

logger = logging.getLogger(__name__)
SENSOR = os.environ.get('SENSOR')
OUTPUT = os.environ.get('OUTPUT')
DB_PATH = os.environ.get('DB_PATH')

def extract_flood(green_band_fp: str,
                  nir_band_fp: str,
                  mtl_fp: str=None):
    """
    Parameters
    ----------
    green_band_fp: Filepath of band3
    nir_band_fp: Filepath of band5
    mtl_fp: Filepath of metadata file
    """
    logger.info('Extracting')
    
    if green_band_fp is None or nir_band_fp is None:
        raise Exception()

    if mtl_fp is not None:
        metadata = utils.build_landsat_metadata(landsat_mtl_fp=mtl_fp)
    
    g_img = utils.load_image(fpath=green_band_fp)
    nir_img = utils.load_image(fpath=nir_band_fp)
    
    g_array, g_profile,_ = utils.image_to_array(img=g_img, masked=True)
    nir_array, nir_profile,_ = utils.image_to_array(img=nir_img, masked=True)
    
    if SENSOR == 'landsat8':
        g_reflect = radiance_to_reflectance(array=g_array,
                                             band=3,
                                             metadata=metadata)
        nir_reflect = radiance_to_reflectance(array=nir_array,
                                             band=5,
                                             metadata=metadata)
    elif SENSOR == 'sentinel2':
        g_reflect = g_array
        nir_reflect = nir_array

    num = g_reflect.__sub__(nir_reflect)
    den = g_reflect.__add__(nir_reflect)
    ndwi = num/den

    if SENSOR=='landsat8':
        water = ma.where(ndwi>0,1,0)
    elif SENSOR=='sentinel2':
        water = ma.where(ndwi<1,1,0)

    out_profile = DefaultGTiffProfile()
    out_profile.update(
    {'width':water.shape[1],
    'height':water.shape[0],
    'count':1,
    'nodata':0
    })
    out_profile.update(crs=g_profile['crs'])

    with rio.open(fp=os.path.join(OUTPUT,f'{SENSOR}-ndwi.tif'),mode='w',**out_profile) as tif:
        tif.write(water,indexes=1)
    return 

def extract_true_color(
        blue_band_fp:str, green_band_fp:str, red_band_fp:str
        ):

    r_img = utils.load_image(fpath=red_band_fp)
    g_img = utils.load_image(fpath=green_band_fp)
    b_img = utils.load_image(fpath=blue_band_fp) 

    r_array, r_profile,_ = utils.image_to_array(
        img=r_img
    )
    g_array, g_profile,_ = utils.image_to_array(
        img=g_img
    )
    b_array, b_profile,_ = utils.image_to_array(
        img=b_img)
    
    filepath = os.path.join(OUTPUT,f'{SENSOR}-truecolor.tif') 

    with rio.open(
        fp=filepath,mode='w',width=b_profile['width'],height=b_profile['height'],
        crs=b_profile['crs'],transform=b_profile['transform'],count=3,dtype=b_profile['dtype']
        ) as tif:
        tif.write(b_array,1)
        tif.write(g_array,2)
        tif.write(r_array,3)

        logger.info(f'Connecting to database')
        cnxn = sqlite3.connect(database=DB_PATH)
        cur = cnxn.cursor()

        cur.execute(f"""
                    INSERT INTO source VALUES
                    ('{uuid4()}','{SENSOR}','{filepath}','{dt.datetime.now().isoformat()}')
                    """)

        cnxn.commit()

        res = cur.execute("SELECT * FROM source")

        logger.debug(res.fetchone())

    return