from tempfile import NamedTemporaryFile
from rasterio.warp import calculate_default_transform, reproject
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

def image_to_array(img: bytes, masked: bool = True, band_idx=int):
    with NamedTemporaryFile(mode='wb',suffix='.tif') as tmp:
        tmp.write(img)
        tmp.seek(0)
        with NamedTemporaryFile() as tmp_array:
            with rio.open(fp=tmp.name) as src:
                profile = src.profile
                logger.debug(profile)
                bounds = src.bounds
                array = np.memmap(
                    filename=tmp_array.name,dtype=profile['dtype'],mode='w+',
                    shape = src.shape
                )
                src.read(band_idx,out=array)
                logger.debug(array.shape)
                
                return array, profile, bounds

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

def build_alos2palsar2_metadata(metadata_fp):
    # collect geocode information
    metadata = {}
    with open(file=metadata_fp,mode='r') as summary:
        for ln in summary.readlines():
            key = ln.split('=')[0]
            try:
                value = float(ln.split('=')[1].replace('"','').strip('\n'))
            except Exception as e:
                try:
                    value = ln.split('=')[1].replace('"','').strip('\n')
                except Exception as e:
                    continue
            metadata[key] = value
    logger.debug(metadata)
    return metadata

def derive_minmax_coords(profile):
    # determine the min and max longitude/easting 
    # and latitude/northing
    width = profile['width']
    height = profile['height']
    gdal_format = profile['transform'].to_gdal()
    logger.debug(gdal_format)
    minx=gdal_format[0]
    maxx=gdal_format[0] + gdal_format[1]*width + gdal_format[1]
    miny=gdal_format[3]
    maxy=gdal_format[3] + gdal_format[5]*height + gdal_format[5]
    logger.debug(f'({minx},{miny},{maxx},{maxy}')
    return (minx,miny,maxx,maxy)

def geocode_alos2palsar2():

    return

def get_earth_sun_distance(data: str):

    distance = None

    for ln in data.readlines():
        if 'EARTH_SUN_DISTANCE' in ln:
            distance = float(ln.split('=')[1].strip(' '))
            logger.debug(type(distance))
            logger.debug(distance)
    return distance

def project_image(band: np.ndarray, src_bounds, src_profile, src_crs, dst_crs):
    logger.debug(src_bounds.top)
    transform,w,h = calculate_default_transform(src_crs=src_crs,
                                                dst_crs=dst_crs,
                                                width=src_profile['width'],
                                                height=src_profile['height'],
                                                left=src_bounds.left,
                                                bottom=src_bounds.bottom,
                                                right=src_bounds.right,
                                                top=src_bounds.top)
    logger.debug((h,w))
    with NamedTemporaryFile() as tmp:
        output = np.memmap(
            filename=tmp.name,dtype=band.dtype,shape=(h,w))
        logger.debug(src_profile['transform'].to_gdal())
        logger.debug(transform.to_gdal())
        logger.debug(band.shape)
        logger.debug(output.shape)
    
        reproject(source=band,
                  destination=output,
                  src_crs=src_crs,
                  dst_crs=dst_crs,
                  src_transform=src_profile['transform'],
                  dst_transform=transform)
        
        return output