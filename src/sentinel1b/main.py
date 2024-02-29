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
    logger.debug(input_dir)
    pre_fn, post_fn = get_pre_post_imgs(indir=input_dir)

    return

if __name__=="__main__":
    main()