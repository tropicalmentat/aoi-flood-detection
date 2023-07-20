import rasterio as rio
import logging

logger = logging.getLogger(__name__)

def test_load(sentinel1b_fp):
    img = None
    with rio.open(fp=sentinel1b_fp) as tif:
        profile = tif.profile
        logger.debug(profile)

    assert False