from shared.preprocess.landsat import radiance_to_reflectance
import os
import numpy.ma as ma
import shared.utils as utils
import logging
import rasterio as rio

logger = logging.getLogger(__name__)
OUTPUT = os.environ.get('OUTPUT')

# TODO: Generalize func signatures for optical imagery
def extract_flood(green_band_fp: str,
                  nir_band_fp: str,
                  mtl_fp: str=None):
    """
    Parameters
    ----------
    green_band_fp: Filepath of band3
    nir_band_fp: Filepath of band5
    mtl_fp: Filepath of metadata file
    """
    logger.info('Extracting')
    
    if green_band_fp is None or nir_band_fp is None:
        raise Exception()

    metadata = utils.build_landsat_metadata(landsat_mtl_fp=mtl_fp)
    
    g_img = utils.load_image(fpath=green_band_fp)
    nir_img = utils.load_image(fpath=nir_band_fp)
    
    g_array, g_profile,_ = utils.image_to_array(img=g_img, masked=True)
    nir_array, nir_profile,_ = utils.image_to_array(img=nir_img, masked=True)
    
    g_reflect = radiance_to_reflectance(array=g_array,
                                         band=3,
                                         metadata=metadata)
    nir_reflect = radiance_to_reflectance(array=nir_array,
                                         band=5,
                                         metadata=metadata)

    num = g_reflect.__sub__(nir_reflect)
    den = g_reflect.__add__(nir_reflect)
    ndwi = num/den
    
    water = ma.where(ndwi>0,1,0)

    water_profile = g_profile.copy()
    water_profile['nodata'] = 0

    with rio.open(fp=os.path.join(OUTPUT,f'landsat-ndwi.tif'),mode='w',**water_profile) as tif:
        tif.write(water,indexes=1)
    return water

def extract_true_color(
        blue_band_fp:str, green_band_fp:str, red_band_fp:str
        ):

    r_img = utils.load_image(fpath=red_band_fp)
    g_img = utils.load_image(fpath=green_band_fp)
    b_img = utils.load_image(fpath=blue_band_fp) 

    r_array, r_profile,_ = utils.image_to_array(
        img=r_img
    )
    g_array, g_profile,_ = utils.image_to_array(
        img=g_img
    )
    b_array, b_profile,_ = utils.image_to_array(
        img=b_img)

    with rio.open(
        fp=os.path.join(OUTPUT,f'landsat-truecolor.tif'),mode='w',width=b_profile['width'],height=b_profile['height'],
        crs=b_profile['crs'],transform=b_profile['transform'],count=3,dtype=b_profile['dtype']
        ) as tif:
        tif.write(b_array,1)
        tif.write(g_array,2)
        tif.write(r_array,3)

    return