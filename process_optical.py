import rasterio as rio
import logging
import numpy as np
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

def image_to_array(img: bytes):
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

                return array, profile

def load_band(fpath):
    img = None

    with rio.open(fp=fpath) as tif:
        profile = tif.profile
        logger.debug(profile)
    return img

def dn_to_radiance(img: bytes):


    return img

def main():
    
    return

if __name__=="__main__":
    main()