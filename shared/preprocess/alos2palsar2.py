import rasterio as rio
import numpy as np
import logging
import otbApplication as otb
from rasterio.warp import calculate_default_transform

logger = logging.getLogger(__name__)

def calibrate_backscatter(band: np.ndarray):
    logger.debug(band)
    backscatter = 20 * np.log10(band) - 82.0
    logger.debug(backscatter.compressed())

    return backscatter

def speckle_filtering(band: np.ndarray):
    logger.debug(band.shape)

    app = otb.Registry.CreateApplication("Despeckle")
    app.SetImageFromNumpyArray('in',band[0])
    app.SetParameterString('filter','lee')
    app.SetParameterInt('filter.lee.rad',3)
    app.Execute()

    filtered = app.GetImageAsNumpyArray('out')

    return filtered

def project_image(band: np.ndarray, src_profile, src_crs, dst_crs):
    src_transform = src_profile['transform'].to_gdal()
    logger.debug(src_transform)
    transform = calculate_default_transform(src_crs=src_crs,
                                            dst_crs=dst_crs,
                                            width=src_profile['width'],
                                            height=src_profile['height'])
    logger.debug(transform)

    return

def main():

    return

if __name__=="__main__":
    main()