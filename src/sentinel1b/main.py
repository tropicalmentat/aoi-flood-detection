import os
import logging
from sys import stdout
from extract import (
    get_pre_post_imgs,
    extract
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

def main():

    input_dir = os.environ.get('INPUT_DIR')
    bounds_fn = os.environ.get('BOUNDS')
    dem = os.environ.get('DEM')

    logger.debug(input_dir)
    logger.debug(bounds_fn)
    logger.debug(dem)
    pre_fn, post_fn = get_pre_post_imgs(indir=input_dir)

    logger.info(f'Pre-image: {pre_fn}, Post-image: {post_fn}')

    extract(pre_safe_fp=pre_fn,post_safe_fp=post_fn,bounds_fp=bounds_fn,dem_fp=dem)
    return

if __name__=="__main__":
    main()