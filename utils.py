from tempfile import NamedTemporaryFile
import rasterio as rio
import numpy as np
import numpy.ma as ma
import logging

logger = logging.getLogger(__name__)

def get_nodata_mask(array: np.ndarray, profile: dict):

    mask = np.where(array==profile['nodata'],True,False)

    return mask

def load_band(fpath):
    img = None

    with rio.open(fp=fpath) as tif:

        profile = tif.profile
        logger.debug(profile)
    return img

def image_to_array(img: bytes, masked: bool = True):
    with NamedTemporaryFile(mode='wb',suffix='.tif') as tmp:
        tmp.write(img)
        tmp.seek(0)
        with NamedTemporaryFile() as tmp_array:
            with rio.open(fp=tmp.name) as src:
                profile = src.profile
    
                array = np.memmap(
                    filename=tmp_array.name,dtype=profile['dtype'],mode='w+',
                    shape = (src.count, *src.shape)
                )
                src.read(masked=True,boundless=True,fill_value=src.nodata,out=array)
                
                if masked==True:
                    return ma.masked_equal(x=array,value=profile['nodata'])
                else:
                    return array, profile