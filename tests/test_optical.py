import logging
import process_optical as po
import rasterio as rio

logger = logging.getLogger(__name__)
logging.getLogger('rasterio').setLevel(logging.CRITICAL)

def test_dn_to_radiance(landsat_band3_masked_array, landsat_band3_profile):
    logger.debug(landsat_band3_masked_array)

    radiance = po.dn_to_radiance(array=landsat_band3_masked_array)

    landsat_band3_profile['dtype'] = 'float64'

    # with rio.open(fp='tests/data/landsat_b3.tiff', mode='w', **landsat_band3_profile) as tif:
        # tif.write(radiance, 1)
    assert False

def test_radiance_to_reflectance(
        landsat_radiance_b3, landsat_metadata
        ):

    reflectance = po.radiance_to_reflectance(
        array=landsat_radiance_b3,band=3,metadata=landsat_metadata
    )

    logger.debug(reflectance)

    assert False

def test_preprocess_landsat():

    processed = po.preprocess_landsat()

    assert False