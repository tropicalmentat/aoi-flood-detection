import pytest
import rasterio as rio
import numpy as np
import numpy.ma as ma
import logging
import pandas as pd
from json import loads

logger = logging.getLogger(__name__)

@pytest.fixture
def pre_goni_cv_opt():
    # optical img for typhoon goni
    # for cagayan valley pre typhoon
    fp = f'./tests/data/s1b-iw-grd-vh-20200914t095832-20200914t095857-023370-02c637-002.tiff'

    return fp

@pytest.fixture
def landsat_mtl_file():

    fp = f'./tests/data/LO08_L1TP_116050_20201106_20201112_01_T1_MTL.txt'

    return fp

@pytest.fixture
def landsat_mtl_data(landsat_mtl_file):

    data = open(file=landsat_mtl_file,mode='r') 
    return data

@pytest.fixture
def MM_LANDSAT8_USGS_20201106_B3():

    fp = f'./tests/data/LO08_L1TP_116050_20201106_20201112_01_T1_B3.tiff'

    return fp

@pytest.fixture
def MM_LANDSAT8_USGS_20201106_B5():

    fp = f'./tests/data/LO08_L1TP_116050_20201106_20201112_01_T1_B5.tiff'

    return fp

@pytest.fixture
def landsat_band3_img(MM_LANDSAT8_USGS_20201106_B3):

    img = None
    with open(file=MM_LANDSAT8_USGS_20201106_B3,mode='rb') as tif:
        img = tif.read()
    return img

@pytest.fixture
def landsat_band3_array(MM_LANDSAT8_USGS_20201106_B3):
    
    array = None

    with rio.open(fp=MM_LANDSAT8_USGS_20201106_B3) as tif:
        array = tif.read(1)
    
    return array

@pytest.fixture
def landsat_band3_masked_array(MM_LANDSAT8_USGS_20201106_B3):

    masked_array = None

    with rio.open(fp=MM_LANDSAT8_USGS_20201106_B3) as tif:
        array = tif.read(1)
        masked_array = ma.masked_equal(x=array,value=0)
    
    return masked_array


@pytest.fixture
def landsat_band3_profile(MM_LANDSAT8_USGS_20201106_B3):

    profile = None

    with rio.open(fp=MM_LANDSAT8_USGS_20201106_B3) as tif:
        profile = tif.profile

    return profile

@pytest.fixture
def nodata_mask(MM_LANDSAT8_USGS_20201106_B3):

    mask = None

    with rio.open(fp=MM_LANDSAT8_USGS_20201106_B3) as tif:
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

    fp = f'./tests/data/landsat_b3.tiff'
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

    fp = f'./tests/data/landsat8_mtl.json'

    metadata = None
    with open(file=fp) as data:
        metadata = loads(data.read())
    return metadata
