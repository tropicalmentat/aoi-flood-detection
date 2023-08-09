from shared.preprocess.alos2palsar2 import (
    calibrate_backscatter,
    speckle_filtering
)
import numpy as np
import shared.utils as utils
import rasterio as rio
import logging

logger = logging.getLogger(__name__)

def extract(img_fp: str):

    img = utils.load_image(fpath=img_fp) 

    array, profile = utils.image_to_array(img=img)

    calibrated = calibrate_backscatter(band=array)

    filtered = speckle_filtering(band=calibrated)

    return