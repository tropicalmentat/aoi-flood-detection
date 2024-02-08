import logging
import numpy as np

from . preprocess import init_datasets
from tempfile import NamedTemporaryFile
from shared.utils import (
    array_to_image
)

logger = logging.getLogger(__name__)

def extract(
        pre_safe_fp,post_safe_fp,bounds_fp,dem_fp
        ):
    
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

        logger.debug(pre_array)

        pre = array_to_image(
            array=pre_array,profile=pre_profile
            )
        post = array_to_image(
            array=post_array,profile=post_profile
        )

    return
