from tempfile import NamedTemporaryFile
import rasterio as rio
import numpy as np
import numpy.ma as ma
import logging

logger = logging.getLogger(__name__)

def get_nodata_mask(array: np.ndarray, profile: dict):

    mask = np.where(array==profile['nodata'],True,False)

    return mask

def load_image(fpath):
    img = None
    with open(file=fpath,mode='rb') as tif:
        img = tif.read()
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
                    return ma.masked_equal(x=array,value=profile['nodata']), profile
                else:
                    return array, profile

def build_landsat_metadata(landsat_mtl_fp):

    metadata = {}
    with open(landsat_mtl_fp) as mtl:
        for ln in mtl.readlines():
            if 'GROUP' in ln: # skip group headers
                continue
            key = ln.split('=')[0].strip(' ')
            # handle the numerical values as float
            # and the string values as text
            try:
                value = float(ln.split('=')[1].strip(' ').strip('\n'))
            except Exception as e:
                # logger.warning(e)
                try:
                    value = ln.split('=')[1].strip(' ').strip('\n') 
                except Exception as e:
                    # logger.error(e)
                    continue
            metadata[key] = value

    return metadata

def get_earth_sun_distance(data: str):

    distance = None

    for ln in data.readlines():
        if 'EARTH_SUN_DISTANCE' in ln:
            distance = float(ln.split('=')[1].strip(' '))
            logger.debug(type(distance))
            logger.debug(distance)
    return distance