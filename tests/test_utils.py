import utils
import logging
from numpy.dtypes import BoolDType

logger = logging.getLogger(__name__)


def test_load_band(MM_LANDSAT8_USGS_20201106_B3):

    img = utils.load_band(MM_LANDSAT8_USGS_20201106_B3)    

    assert False

def test_img_to_array(landsat_band3_img):

    array, profile = utils.image_to_array(img=landsat_band3_img)
    logger.debug(array)
    logger.debug(profile)
    assert array is not None and profile is not None

def test_get_nodata_mask(landsat_band3_array, landsat_band3_profile):

    nodata_array = utils.get_nodata_mask(
        array=landsat_band3_array, profile=landsat_band3_profile
        )

    logger.debug(nodata_array)

    assert isinstance(nodata_array.dtype,BoolDType)