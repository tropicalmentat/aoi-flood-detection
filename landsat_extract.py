from preprocess.landsat import radiance_to_reflectance
import numpy.ma as ma
import utils
import logging
import rasterio as rio

logger = logging.getLogger(__name__)

def extract(band3_fp: str,
            band5_fp: str,
            mtl_fp: str):
    
    if band3_fp is None or band5_fp is None:
        raise Exception()

    metadata = utils.build_preprocess_metadata(landsat_mtl_fp=mtl_fp)
    
    b3_img = utils.load_image(fpath=band3_fp)
    b5_img = utils.load_image(fpath=band5_fp)
    
    b3_array, b3_profile = utils.image_to_array(img=b3_img, masked=True)
    b5_array, b5_profile = utils.image_to_array(img=b5_img, masked=True)
    
    b3_reflect = radiance_to_reflectance(array=b3_array,
                                         band=3,
                                         metadata=metadata)
    b5_reflect = radiance_to_reflectance(array=b5_array,
                                         band=5,
                                         metadata=metadata)

    num = b3_reflect.__sub__(b5_reflect)
    den = b3_reflect.__add__(b5_reflect)
    ndwi = num/den
    
    water = ma.where(ndwi>0,1,0)

    water_profile = b3_profile.copy()
    water_profile['nodata'] = 9999

    # with rio.open(fp=f'./tests/data/ndwi.tif',mode='w',**water_profile) as tif:
        # tif.write(water)
    return ndwi