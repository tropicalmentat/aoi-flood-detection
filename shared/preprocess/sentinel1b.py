from sarsen import apps
import xarray as xr
import logging

logger = logging.getLogger(__name__)
logging.getLogger("xmlschema").setLevel(logging.CRITICAL)

def geocode_img(fp):
    calibration_group = "IW/VH/calibration"
    measurement_group = 'IW/VH'
    orbit_group = f'{measurement_group}/orbit'
    kwargs = {'chunks':2048}

    calibration = xr.open_dataset(
        fp,engine="sentinel-1",group=calibration_group,**kwargs)
    beta_nought_lut = calibration.betaNought

    measurement_ds = xr.open_dataset(
        fp, engine='sentinel-1', group=measurement_group,**kwargs)
    measurement = measurement_ds.measurement
    
    orbit_ecef = xr.open_dataset(
        fp,engine='sentinel-1', group=orbit_group, **kwargs
    )
    position_ecef = orbit_ecef.position

    logger.debug(measurement)
    logger.debug(calibration)
    logger.debug(orbit_ecef)
    logger.debug(position_ecef)
    return