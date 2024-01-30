from shared.preprocess.sentinel1b import (
    geocode_img
)
import os
import pytest
import logging
import rasterio as rio
import shared.utils as utils

logger = logging.getLogger(__name__)

def test_geocode(sentinel1b_post_fp):

    geocoded = geocode_img(sentinel1b_post_fp)

    assert False

def test_init_lut(sentinel1b_post_fp_measurement):

    with rio.open(fp=sentinel1b_post_fp_measurement) as src:
        logger.debug(src.profile)

    assert False