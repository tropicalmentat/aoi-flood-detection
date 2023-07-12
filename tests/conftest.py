import pytest
import rasterio as rio

@pytest.fixture
def pre_goni_cv_opt():
    # optical img for typhoon goni
    # for cagayan valley pre typhoon
    fp = f'./tests/data/s1b-iw-grd-vh-20200914t095832-20200914t095857-023370-02c637-002.tiff'

    return fp

@pytest.fixture
def MM_LANDSAT8_USGS_20201106_B3():

    fp = f'./tests/data/LO08_L1TP_116050_20201106_20201112_01_T1_B3.tiff'

    return fp

@pytest.fixture
def MM_LANDSAT8_USGS_20201106_B5():

    fp = f'./tests/data/LO08_L1TP_116050_20201106_20201112_01_T1_B5.tiff'

    return fp

@pytest.fixture
def landsat_band3(MM_LANDSAT8_USGS_20201106_B3):

    img = None
    with open(file=MM_LANDSAT8_USGS_20201106_B3,mode='rb') as tif:
        img = tif.read()
    return img