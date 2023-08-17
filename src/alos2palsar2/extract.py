from shared.preprocess.alos2palsar2 import (
    calibrate_backscatter,
    speckle_filtering
)
from shared.utils import get_nodata_mask
from tempfile import NamedTemporaryFile
from io import BytesIO
import numpy as np
import shared.utils as utils
import rasterio as rio
import logging

logger = logging.getLogger(__name__)

def get_preprocessed(img_fp):

    img = None
    with NamedTemporaryFile() as tmp, rio.MemoryFile(tmp) as mem:
        img = utils.load_image(fpath=img_fp) 
    
        array, profile = utils.image_to_array(img=img,band_idx=1)
    
        calibrated = calibrate_backscatter(band=array)
    
        filtered = speckle_filtering(band=calibrated)
        calibrated = None
        masked = np.ma.masked_outside(x=filtered,v1=round(filtered.max(),2),v2=-99.0)
        filtered = None
        logger.debug(masked.compressed())
        casted = masked.astype(dtype='float32', casting='same_kind', copy=False)
        filled = (np.ma.filled(a=casted,fill_value=-9999.0))[:]
        casted = None
        profile.update({'dtype':filled.dtype})
        profile.update(compression='lzw')
        with mem.open(
            driver='GTiff',width=profile['width'],height=profile['height'],
            count=profile['count'],dtype=profile['dtype']) as src:
            src.write(filled,1)
        img = mem.read()
    return img 

def extract(pre_img:str, post_img:str):

    pre = get_preprocessed(pre_img)
    logger.debug(len(pre))

    return