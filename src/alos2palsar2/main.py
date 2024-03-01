import os
import logging

from tempfile import TemporaryDirectory
from extract import (
    get_pre_post_imgs,
    extract
)
from sys import stdout

logger = logging.getLogger(__name__)

logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

def main():
    logger.info('Start')
    input_dir = os.environ.get('INPUT_DIR')
    logger.debug(input_dir)

    with TemporaryDirectory() as tmp_dir:
        pre_fn, post_fn = get_pre_post_imgs(indir=input_dir,tmpdir=tmp_dir)

        if os.path.exists(pre_fn): 
            logger.info(f'Pre-event image detected: {pre_fn}')
        else:
            raise FileNotFoundError()

        if os.path.exists(post_fn): 
            logger.info(f'Pre-event image detected: {post_fn}')
        else:
            raise FileNotFoundError()
        
        extract(pre_fp=pre_fn,post_fp=post_fn)

    return

if __name__=="__main__":
    main()