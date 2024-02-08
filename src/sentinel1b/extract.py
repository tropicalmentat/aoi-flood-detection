import logging
import numpy as np
import rasterio as rio

from rasterio.vrt import WarpedVRT
from . preprocess import init_datasets
from tempfile import NamedTemporaryFile
from shared.utils import (
    array_to_image
)

logger = logging.getLogger(__name__)

def extract(
        pre_safe_fp,post_safe_fp,bounds_fp,dem_fp
        ):
    
    pre_img = None
    post_img = None
    pre_profile = None
    post_profile = None
    with NamedTemporaryFile() as pre_mem,\
         NamedTemporaryFile() as post_mem:
        pre_array, pre_profile = init_datasets(
            safe_fp=pre_safe_fp,bounds_fp=bounds_fp,dem_fp=dem_fp,
            memmap_fn=pre_mem.name
        )

        post_array, post_profile = init_datasets(
            safe_fp=post_safe_fp,bounds_fp=bounds_fp,dem_fp=dem_fp,
            memmap_fn=post_mem.name
        )

        logger.info('Performing image differencing')

        pre_img = array_to_image(
            array=pre_array,profile=pre_profile
            )
        post_img = array_to_image(
            array=post_array,profile=post_profile
        )

    # TODO need common vrt profile
    with rio.MemoryFile(file_or_bytes=pre_img) as pre_memf,\
         rio.MemoryFile(file_or_bytes=post_img) as post_memf,\
         pre_memf.open() as pre_src,\
         post_memf.open() as pst_src,\
         WarpedVRT(src_dataset=pre_src,**pre_src.profile) as pre_vrt,\
         WarpedVRT(src_dataset=pst_src,**pst_src.profile) as pst_vrt:
        logger.debug(pre_vrt.profile)
        logger.debug(pst_vrt.profile)

    return
