import logging
import process_optical as po

logger = logging.getLogger(__name__)
logging.getLogger('rasterio').setLevel(logging.CRITICAL)

def test_load_band(MM_LANDSAT8_USGS_20201106_B3):

    img = po.load_band(MM_LANDSAT8_USGS_20201106_B3)    

    assert False

def test_img_to_array(landsat_band3):

    array, profile = po.image_to_array(img=landsat_band3)
    logger.debug(array)
    logger.debug(profile)
    assert False