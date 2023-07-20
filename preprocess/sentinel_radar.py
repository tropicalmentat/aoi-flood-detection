import rasterio as rio
import numpy as np
import logging

logger = logging.getLogger(__name__)

def calibrate_backscatter(band: np.ndarray):
    logger.debug(band)
    backscatter = 10 * np.log10(np.square(band)) - 82.0
    logger.debug(backscatter)

    return

def speckle_filtering():

    return

def main():

    return

if __name__=="__main__":
    main()