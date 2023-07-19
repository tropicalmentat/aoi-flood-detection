import utils
import logging
from json import dumps
from numpy.dtypes import BoolDType

logger = logging.getLogger(__name__)


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

def test_build_metadata(landsat_mtl_fp):

    metadata = utils.build_preprocess_metadata(landsat_mtl_fp)

    logger.debug(metadata)
    with open(file=f'./tests/data/landsat8_mtl.json',mode='w') as mt:
        mt.write(dumps(metadata))

    assert False
