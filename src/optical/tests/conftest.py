import pytest
import rasterio as rio
import numpy as np
import numpy.ma as ma
import logging
import pandas as pd
from json import loads
from rasterio.windows import Window

logger = logging.getLogger(__name__)

@pytest.fixture
def sentinel1b_fp():
    # radar img for typhoon goni
    # for cagayan valley pre typhoon
    fp = f'./tests/data/SENTINEL1/s1b-iw-grd-vh-20200914t095832-20200914t095857-023370-02c637-002.tiff'

    return fp

@pytest.fixture
def sentinel1b_img(sentinel1b_fp):

    img = open(sentinel1b_fp,mode='rb')

    return img

@pytest.fixture
def sentinel1b_band(sentinel1b_img):
    window = Window(col_off=0,row_off=0,width=500,height=500)
    masked = None
    with rio.MemoryFile(sentinel1b_img) as img:
        with img.open() as tif:
            band = tif.read(window=window)
            masked = ma.masked_where(band==0,band,copy=False)

    return masked

@pytest.fixture
def alos2_palsar2_fp():

    fp = f'./tests/data/ALOS2-PALSAR2/IMG-HH-ALOS2350060270-201115-FBDR2.1GUA.tiff'
    return fp

@pytest.fixture
def alos2_palsar2_img(alos2_palsar2_fp):
    img = None
    with open(file=alos2_palsar2_fp,mode='rb') as tif:
        img = tif.read()
    return img

@pytest.fixture
def alos2_palsar2_band(alos2_palsar2_img):
    window = Window(col_off=1000,row_off=5000,width=500,height=500)
    masked = None
    with rio.MemoryFile(file_or_bytes=alos2_palsar2_img) as img:
        with img.open() as tif:
            band = tif.read(window=window)
            logger.debug(tif.profile)
            logger.debug(band)
            masked = ma.masked_where(condition=band==0,a=band,copy=False)
    return masked

@pytest.fixture
def landsat_mtl_fp():

    fp = f'./tests/data/LANDSAT8/LO08_L1TP_116050_20201106_20201112_01_T1_MTL.txt'

    return fp

@pytest.fixture
def landsat_mtl_data(landsat_mtl_fp):

    data = open(file=landsat_mtl_fp,mode='r') 
    return data

@pytest.fixture
def landsat_b2_fp():

    fp = f'./tests/data/LANDSAT8/LO08_L1TP_116050_20201106_20201112_01_T1_B2.tiff'

    return fp

@pytest.fixture
def landsat_b3_fp():

    fp = f'./tests/data/LANDSAT8/LO08_L1TP_116050_20201106_20201112_01_T1_B3.tiff'

    return fp

@pytest.fixture
def landsat_b4_fp():

    fp = f'./tests/data/LANDSAT8/LO08_L1TP_116050_20201106_20201112_01_T1_B4.tiff'

    return fp

@pytest.fixture
def landsat_b5_fp():

    fp = f'./tests/data/LANDSAT8/LO08_L1TP_116050_20201106_20201112_01_T1_B5.tiff'

    return fp

@pytest.fixture
def landsat_band3_img(landsat_b3_fp):

    img = None
    with open(file=landsat_b3_fp,mode='rb') as tif:
        img = tif.read()
    return img

@pytest.fixture
def landsat_band3_array(landsat_b3_fp):
    
    array = None

    with rio.open(fp=landsat_b3_fp) as tif:
        array = tif.read(1)
    
    return array

@pytest.fixture
def landsat_band3_masked_array(landsat_b3_fp):

    masked_array = None

    with rio.open(fp=landsat_b3_fp) as tif:
        array = tif.read(1)
        masked_array = ma.masked_equal(x=array,value=0)
    
    return masked_array


@pytest.fixture
def landsat_band3_profile(landsat_b3_fp):

    profile = None

    with rio.open(fp=landsat_b3_fp) as tif:
        profile = tif.profile

    return profile

@pytest.fixture
def nodata_mask(landsat_b3_fp):

    mask = None

    with rio.open(fp=landsat_b3_fp) as tif:
        array = tif.read(1)
        mask = np.where(array==tif.profile['nodata'],True,False)

    return mask

@pytest.fixture
def earth_sun_distance():
    # earth-sun-distance for the date
    # 2020-11-06
    return 0.9912142

@pytest.fixture
def landsat_radiance_b3():

    fp = f'./tests/data/LANDSAT/landsat_b3.tiff'
    masked_array = None
    with rio.open(fp=fp) as tif:
        array = tif.read(1)
        masked_array = ma.masked_equal(x=array,value=0)
    return masked_array

@pytest.fixture
def esun():
    # mean solar exo-atmospheric irradiances
    # for 2022-11-06

    return 1842

@pytest.fixture
def landsat_metadata():

    fp = f'./tests/data/LANDSAT8/landsat8_mtl.json'

    metadata = None
    with open(file=fp) as data:
        metadata = loads(data.read())
    return metadata
