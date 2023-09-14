from sarsen import apps
import xarray as xr
import logging

logger = logging.getLogger(__name__)
logging.getLogger("xmlschema").setLevel(logging.CRITICAL)

def geocode_img(sentinel1b_post_fp):
    calibration_group = "IW/VH/calibration"
    calibration = xr.open_dataset(
        sentinel1b_post_fp,engine="sentinel-1",group=calibration_group)

    logger.debug(calibration)

    return