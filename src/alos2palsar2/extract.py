from shared.preprocess.alos2palsar2 import (
    calibrate_backscatter,
    despeckle
)
from tempfile import NamedTemporaryFile
from skimage.morphology import square
from skimage.filters.rank import majority
from rasterio.features import shapes
# from osgeo.gdal import Polygonize
from json import dumps
import numpy as np
import shared.utils as utils
import rasterio as rio
import logging
import os

logger = logging.getLogger(__name__)

def get_preprocessed(img_fp, block_size:int=1024):

    img = utils.load_image(fpath=img_fp) 
    # TODO: Create memory mapped output array

    with NamedTemporaryFile() as tmp_bs, \
         NamedTemporaryFile() as tmp_ds, \
         rio.MemoryFile(file_or_bytes=img) as mem, \
         mem.open() as src:

        profile = src.profile

        calibrated = np.memmap(
            filename=tmp_bs.name, dtype=np.float16,
            shape=(profile.get('height'),profile.get('width'))
        )

        despeckled = np.memmap(
            filename=tmp_ds.name, dtype=np.float16,
            shape=(profile.get('height'),profile.get('width'))
        )

        offsets, col_offs, row_offs = utils.get_window_offsets(
            img=img, block_size=block_size
        )
    
        slices = []
        for i,pair in enumerate(offsets,start=1):
            logger.info(f'Calibrate window {i}')
            array = None
            transform = None
            if pair[0] == col_offs[-1] or pair[1] == row_offs[-1]:
                array, transform, slice = utils.window_to_array(
                    src=src, offset_pair=pair,block_size=block_size
                )
                calibrated[slice] = 20 * np.log10(array) - 83.0
                slices.append(slice)
            else:
                array, transform, slice = utils.window_to_array(
                    src=src, offset_pair=pair,block_size=block_size,
                    edge=False
                )
                calibrated[slice] = 20 * np.log10(array) - 83.0
                slices.append(slice)

        for i,slice in enumerate(slices,start=1):
            logger.info(f'Despeckle window {i}')
            # TODO: Despeckle with buffered slice
            despeckled[slice] = despeckle(band=calibrated[slice])
            masked = np.ma.masked_outside(x=despeckled[slice],v1=round(despeckled[slice].max(),2),v2=-99.0)
            logger.debug(masked.compressed())
    """
        # TODO: despeckle needs buffered windows
        despeckled = despeckle(band=calibrated)
        calibrated = None
        masked = np.ma.masked_outside(x=despeckled,v1=round(despeckled.max(),2),v2=-99.0)
        despeckled = None
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
    """
    
    # return preprocessed, profile, bounds 

def extract(pre_fp:str, post_fp:str, cols=None, rows=None):

    with NamedTemporaryFile() as pre_tmp, NamedTemporaryFile() as post_tmp:
        pre,pre_profile,pre_bounds = get_preprocessed(pre_fp, cols=cols, rows=rows)

        post,post_profile,post_bounds = get_preprocessed(post_fp, cols=cols, rows=rows)
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
            filename=post_tmp.name,dtype='float32',mode='r',shape=(pre_profile['height'],pre_profile['width'])
        )

        diff = np.ma.masked_equal(
            post_mem,value=pre_profile['nodata']) - np.ma.masked_equal(pre_mem,value=pre_profile['nodata'])

        logger.info(f'Applying threshold')

        threshold = np.ma.where(diff<-3,1,0)

        logger.info(f'Applying majority filter')

        filtered = majority(image=threshold,footprint=square(width=5))

        logger.info(f'Extracting flood pixels as vector features')

        features = shapes(source=filtered,transform=pre_profile['transform'])

        logger.info(f'Converting to FeatureCollection')

        flood = {'type':'FeatureCollection',
                 'features':[]}

        for feat in features:
            if feat[1] == 1.0:
                feature = {'type':'Feature', 
                           'geometry':feat[0],
                           'properties':{
                                'value':1.0
                            }
                            }
                flood['features'].append(feature)

        # projected = utils.project_image(
        #     band=filtered,src_bounds=pre_bounds,src_profile=pre_profile,src_crs=pre_profile['crs'],dst_crs=rio.CRS.from_epsg(32651)
        #     )
        # logger.debug(projected)
        # logger.debug(projected.dtype)

        # with rio.open(
        #     fp=f'./tests/data/filtered.tiff',mode='w',
        #     width=pre_profile['width'],height=pre_profile['height'],count=1,dtype='int16',
        #     transform=pre_profile['transform'],crs=pre_profile['crs'],compress='lzw'
        # ) as tmp:
        #     tmp.write(projected,1)
    return flood