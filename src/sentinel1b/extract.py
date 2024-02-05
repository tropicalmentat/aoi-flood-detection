import logging
from . preprocess import init_datasets

from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

def extract(
        pre_safe_fp,post_safe_fp,bounds_fp,dem_fp
        ):
    
    with NamedTemporaryFile() as pre_mem,\
         NamedTemporaryFile() as post_mem:
        pre_img, pre_profile = init_datasets(
            safe_fp=pre_safe_fp,bounds_fp=bounds_fp,dem_fp=dem_fp,
            memmap_fn=pre_mem.name
        )

        post_img, post_profile = init_datasets(
            safe_fp=post_safe_fp,bounds_fp=bounds_fp,dem_fp=dem_fp,
            memmap_fn=post_mem.name
        )
    

    return
