import rasterio as rio
import logging
import shared.preprocess.radar as ap 

logger = logging.getLogger(__name__)
logging.getLogger('rasterio').setLevel(logging.CRITICAL)

def test_calibration_to_backscatter(alos2palsar2_band):
    band, profile = alos2palsar2_band
    
    calibrated = ap.calibrate_backscatter(band=band) 

    logger.debug(calibrated.min())
    logger.debug(calibrated.max())

    assert alos2palsar2_band.min() != calibrated.min()

def test_despeckle(alos2palsar2_band):
    band,profile = alos2palsar2_band
    
    despeckled = ap.despeckle(band=band) 

    logger.debug(despeckled)

    assert False

def test_project_img(alos2palsar2_band):
    band,profile,bounds = alos2palsar2_band
    src_crs = profile['crs']
    dst_crs = rio.CRS.from_epsg(4326)
    logger.debug(dst_crs)
    projected = ap.project_image(band=band,
                                 src_profile=profile,
                                 src_bounds=bounds,
                                 src_crs=src_crs,
                                 dst_crs=dst_crs)
# 
    assert False