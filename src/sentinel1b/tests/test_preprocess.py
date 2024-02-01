from shared.preprocess.sentinel1b import (
    geocode_img,
    download_dem
)
import os
import pytest
import logging
import rasterio as rio
import shared.utils as utils
import xml.etree.ElementTree as ET
from sarsen import Sentinel1SarProduct

logger = logging.getLogger(__name__)

def test_geocode(sentinel1b_post_fp):

    geocoded = geocode_img(sentinel1b_post_fp)

    assert False

def test_init_lut(sentinel1b_post_fp_measurement):

    with rio.open(fp=sentinel1b_post_fp_measurement) as src:
        logger.debug(src.profile)

    assert False

def test_get_elevation(sentinel1b_post_fp_manifest,sentinel1b_post_fp):

    logger.debug(sentinel1b_post_fp_manifest)
    tree = ET.parse(sentinel1b_post_fp_manifest)
    root = tree.getroot()

    for child in root:
        if 'metadata' in child.tag:
            for gc in child:
                if 'measurementFrameSet' in gc.attrib.get('ID'):
                    for subelm in gc.iter():
                        if 'coordinates' in subelm.tag:
                            logger.debug(subelm.text)
                            raw = [pair.split(',') for pair in subelm.text.split(' ')]
                            bbox = [(float(pair[0]),float(pair[1])) for pair in raw]
                            logger.debug(bbox)
    
    assert False