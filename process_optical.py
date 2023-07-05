import rasterio as rio
import logging

logger = logging.getLogger(__name__)

def load_img(fpath):
    img = None

    with rio.open(fp=fpath) as tif:
        profile = tif.profile
        logger.debug(profile)
    return img

def main():
    
    return

if __name__=="__main__":
    main()