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
def alos2palsar2_fp():

    fp = f'./tests/data/ALOS2-PALSAR2/IMG-HH-ALOS2350060270-201115-FBDR2.1GUA.tiff'
    return fp

@pytest.fixture
def alos2palsar2_img(alos2palsar2_fp):
    img = None
    with open(file=alos2palsar2_fp,mode='rb') as tif:
        img = tif.read()
    return img

@pytest.fixture
def alos2palsar2_band(alos2palsar2_img):
    window = Window(col_off=1000,row_off=5000,width=500,height=500)
    masked = None
    profile = None
    with rio.MemoryFile(file_or_bytes=alos2palsar2_img) as img:
        with img.open() as tif:
            band = tif.read(window=window)
            profile = tif.profile
            logger.debug(tif.profile)
            logger.debug(band)
            masked = ma.masked_where(condition=band==0,a=band,copy=False)
    return masked, profile

@pytest.fixture
def alos2palsar2_summary_fp():

    fp = f'./tests/data/ALOS2-PALSAR2/summary.txt'

    return fp