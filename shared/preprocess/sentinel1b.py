from sarsen import apps
import xarray as xr
import logging

logger = logging.getLogger(__name__)
logging.getLogger("xmlschema").setLevel(logging.CRITICAL)

def geocode_img(fp):
    calibration_group = "IW/VH/calibration"
    measurement_group = 'IW/VH'
    kwargs = {'chunks':2048}

    calibration = xr.open_dataset(
        fp,engine="sentinel-1",group=calibration_group,**kwargs)

    measurement_ds = xr.open_dataset(
        fp, engine='sentinel-1', group=measurement_group,**kwargs)
    measurement = measurement_ds.measurement

    logger.debug(measurement)
    logger.debug(calibration)
    logger.debug(calibration.betaNought)
    return