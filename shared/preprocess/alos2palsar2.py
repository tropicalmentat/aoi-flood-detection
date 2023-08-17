import rasterio as rio
import numpy as np
import logging
import otbApplication as otb
from rasterio.warp import (
    calculate_default_transform, reproject
    )
from tempfile import NamedTemporaryFile
from shared.utils import derive_minmax_coords

logger = logging.getLogger(__name__)

def calibrate_backscatter(band: np.ndarray):
    backscatter = 20 * np.log10(band) - 83.0

    return backscatter

def speckle_filtering(band: np.ndarray):
    input = band.astype(dtype='float64')

    app = otb.Registry.CreateApplication("Despeckle")
    app.SetImageFromNumpyArray('in',input)
    app.SetParameterString('filter','lee')
    app.SetParameterInt('filter.lee.rad',1)
    app.SetParameterInt('filter.lee.nblooks',1)
    app.Execute()

    filtered = app.GetImageAsNumpyArray('out')
    casted = filtered.astype(dtype='float64',copy=False)
    return casted

def project_image(band: np.ndarray, src_bounds, src_profile, src_crs, dst_crs):
    logger.debug(src_bounds.top)
    transform,w,h = calculate_default_transform(src_crs=src_crs,
                                                dst_crs=dst_crs,
                                                width=src_profile['width'],
                                                height=src_profile['height'],
                                                left=src_bounds.left,
                                                bottom=src_bounds.bottom,
                                                right=src_bounds.right,
                                                top=src_bounds.top)
    logger.debug((h,w))
    with NamedTemporaryFile() as tmp:
        output = np.memmap(
            filename=tmp.name,dtype=band.dtype,shape=band[0].shape)
        logger.debug(src_profile['transform'])
        logger.debug(transform)
        logger.debug(band.shape)
        logger.debug(output.shape)

        # with rio.open(fp='./test.tif',mode='w',width=w,height=h,count=1,crs=dst_crs,transform=transform,dtype=band.dtype) as tif:
        #     tif.write(band)
        # warped = reproject(source=band[0],
                        #    destination=output,
                        #    src_crs=src_crs,
                        #    dst_crs=dst_crs,
                        #    src_transform=src_profile['transform'],
                        #    dst_transform=transform,
                        #    warp_mem_limit=1000)
    
    return

def main():

    return

if __name__=="__main__":
    main()