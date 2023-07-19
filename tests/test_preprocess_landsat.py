import logging
import preprocess_landsat as pl
import rasterio as rio

logger = logging.getLogger(__name__)
logging.getLogger('rasterio').setLevel(logging.CRITICAL)

def test_dn_to_radiance(landsat_band3_masked_array, landsat_metadata, landsat_band3_profile):
    logger.debug(landsat_band3_masked_array)

    radiance = pl.dn_to_radiance(
        array=landsat_band3_masked_array,band=3,metadata=landsat_metadata)
    landsat_band3_profile['dtype'] = 'float64'

    # with rio.open(fp='tests/data/landsat_b3.tiff', mode='w', **landsat_band3_profile) as tif:
        # tif.write(radiance, 1)
    assert False

def test_radiance_to_reflectance(
        landsat_band3_masked_array, landsat_metadata, landsat_band3_profile
        ):

    reflectance = pl.radiance_to_reflectance(
        array=landsat_band3_masked_array,band=3,metadata=landsat_metadata
    )

    logger.debug(reflectance.min())
    logger.debug(reflectance.max())

    with rio.open(fp='tests/data/landsat_b3_reflectance.tiff', mode='w', **landsat_band3_profile) as tif:
        tif.write(reflectance, 1)
    assert False

def test_preprocess_landsat():

    assert False