import logging
import process_optical as po

logger = logging.getLogger(__name__)
logging.getLogger('rasterio').setLevel(logging.CRITICAL)

def test_dn_to_radiance(landsat_band3_array):
    logger.debug(landsat_band3_array)

    radiance = po.dn_to_radiance(landsat_band3_array)

    logger.debug(radiance)

    assert False