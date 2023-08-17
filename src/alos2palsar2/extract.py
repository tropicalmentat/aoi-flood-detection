from shared.preprocess.alos2palsar2 import (
    calibrate_backscatter,
    speckle_filtering
)
from tempfile import NamedTemporaryFile
from skimage.morphology import square
from skimage.filters.rank import majority
import numpy as np
import shared.utils as utils
import rasterio as rio
import logging

logger = logging.getLogger(__name__)

def get_preprocessed(img_fp):

    preprocessed = None

    with NamedTemporaryFile() as tmp:
        img = utils.load_image(fpath=img_fp) 
    
        array, profile = utils.image_to_array(img=img,band_idx=1)
    
        calibrated = calibrate_backscatter(band=array)
    
        filtered = speckle_filtering(band=calibrated)
        calibrated = None
        masked = np.ma.masked_outside(x=filtered,v1=round(filtered.max(),2),v2=-99.0)
        filtered = None
        logger.debug(masked.compressed())
        casted = masked.astype(dtype='float32', casting='same_kind', copy=False)
        filled = np.memmap(
            filename=tmp.name,dtype=casted.dtype,shape=casted.shape
        )
        filled[:] = (np.ma.filled(a=casted,fill_value=-9999.0))[:]
        casted = None
        profile.update({'dtype':filled.dtype})
        filled.flush()
        tmp.seek(0)
        preprocessed = tmp.read()
    
    return preprocessed, profile 

def extract(pre_fp:str, post_fp:str):

    with NamedTemporaryFile() as pre_tmp, NamedTemporaryFile() as post_tmp:
        pre,pre_profile = get_preprocessed(pre_fp)

        post,post_profile = get_preprocessed(post_fp)
        logger.debug(len(pre))
        logger.debug(len(post))
        pre_tmp.write(pre)
        post_tmp.write(post)

        pre_tmp.seek(0)
        post_tmp.seek(0)

        pre_mem = np.memmap(
            filename=pre_tmp.name,dtype='float32',mode='r',shape=(pre_profile['height'],pre_profile['width'])
        )
        post_mem = np.memmap(
            filename=post_tmp.name,dtype='float32',mode='r',shape=(post_profile['height'],post_profile['width'])
        )

        diff = np.ma.masked_equal(
            post_mem,value=pre_profile['nodata']) - np.ma.masked_equal(pre_mem,value=pre_profile['nodata'])

        threshold = np.ma.where(diff<-3,1,0)

        filtered = majority(image=threshold,footprint=square(width=5))
        logger.debug(filtered)

        with rio.open(
            fp=f'./tests/data/filtered.tiff',mode='w',
            width=pre_profile['width'],height=pre_profile['height'],count=1,dtype='int16',
            transform=pre_profile['transform'],crs=pre_profile['crs'],compress='lzw'
        ) as tmp:
            tmp.write(filtered,1)
    return