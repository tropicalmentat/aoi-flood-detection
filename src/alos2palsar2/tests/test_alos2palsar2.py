import rasterio as rio
import shared.utils
import logging
import shared.preprocess.alos2palsar2 as ap 

logger = logging.getLogger(__name__)

def test_calibration_to_backscatter(alos2_palsar2_band):
    
    calibrated = ap.calibrate_backscatter(band=alos2_palsar2_band) 

    logger.debug(calibrated.min())
    logger.debug(calibrated.max())

    assert alos2_palsar2_band.min() != calibrated.min()