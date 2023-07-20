import rasterio as rio
import utils
import logging
import preprocess.sentinel_radar as sr 

logger = logging.getLogger(__name__)

def test_calibration_to_backscatter(sentinel1b_band):
    
    calibrated = sr.calibrate_backscatter(band=sentinel1b_band) 
    
    assert False