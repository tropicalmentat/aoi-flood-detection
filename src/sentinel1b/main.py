import os
import logging
from sys import stdout
from extract import (
    get_pre_post_imgs,
    extract
)

logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

def main():

    input_dir = os.environ.get('INPUT_DIR')
    bounds_fn = os.environ.get('BOUNDS')
    dem = os.environ.get('DEM')

    # Check if boundary and DEM files exist
    if os.path.exists(bounds_fn):
        logger.info(f'Boundary SHP file detected: {bounds_fn}')
    else:
        logger.error('Boundary SHP file not found!')
        raise FileNotFoundError()
    if os.path.exists(dem):
        logger.info(f'Digital Elevation file detected: {dem}')
    else:
        logger.error('DEM file not found!')
        raise FileNotFoundError()

    pre_fn, post_fn = get_pre_post_imgs(indir=input_dir)

    if os.path.exists(pre_fn):
        logger.info(f'Pre-event image detected: {pre_fn}')
    else:
        logger.error('Pre-event image not found!')
        raise FileNotFoundError()
    if os.path.exists(post_fn):
        logger.info(f'Post-event image detected: {post_fn}')
    else:
        logger.error('Post-event image not found!')
        raise FileNotFoundError()

    logger.info(f'Extracting flood from pre and post event images')
    extract(pre_safe_fp=pre_fn,post_safe_fp=post_fn,bounds_fp=bounds_fn,dem_fp=dem)
    return

if __name__=="__main__":
    main()