import os
import logging
import numpy as np
import rasterio as rio
import datetime as dt
import sqlite3

from uuid import uuid4
from rasterio.profiles import DefaultGTiffProfile
from rasterio.vrt import WarpedVRT
from rasterio import shutil as rio_shutil
from preprocess import init_datasets
from tempfile import NamedTemporaryFile
from shared.utils import (
    array_to_image
)
from skimage.morphology import square
from skimage.filters.rank import majority

logger = logging.getLogger(__name__)
OUTPUT_DIR = os.environ.get('OUTPUT')
DB_PATH = os.environ.get('DB_PATH')
EVENT = os.environ.get("EVENT")
LOCATION = os.environ.get("LOCATION")

def get_pre_post_imgs(indir):

    pre_fn = None
    post_fn = None
    img_idx = {}
    for fn in os.listdir(indir):
        logger.debug(fn)
        start_capture = fn.split('_')[4].split('T')[0]
        img_idx[dt.datetime.strptime(start_capture,"%Y%m%d")] = fn
    
    sorted_keys = sorted(img_idx)
    pre_fn = img_idx[sorted_keys[0]]
    post_fn = img_idx[sorted_keys[1]]

    return os.path.join(indir,pre_fn), os.path.join(indir,post_fn)

def extract(
        pre_safe_fp,post_safe_fp,bounds_fp,dem_fp
        ):
    
    pre_img = None
    post_img = None
    pre_profile = None
    post_profile = None
    with NamedTemporaryFile() as pre_mem,\
         NamedTemporaryFile() as post_mem:
        pre_array, pre_profile = init_datasets(
            safe_fp=pre_safe_fp,bounds_fp=bounds_fp,dem_fp=dem_fp,
            memmap_fn=pre_mem.name
        )

        post_array, post_profile = init_datasets(
            safe_fp=post_safe_fp,bounds_fp=bounds_fp,dem_fp=dem_fp,
            memmap_fn=post_mem.name
        )

        # with rio.open(
        #     fp=f'./tests/data/naga-post-post-processed.tiff',mode='w',
        #     **post_profile
        # ) as tmp_src:
        #     tmp_src.write(post_array,1)

        logger.info('Performing image differencing')

        pre_img = array_to_image(
            array=pre_array,profile=pre_profile
            )
        post_img = array_to_image(
            array=post_array,profile=post_profile
        )
        
        # with open(file=f'./tests/data/naga-post-array2image.tiff',mode='wb') as tmp_post:
        #     tmp_post.write(post_img)

    vrt_profile = {
        'transform':post_profile['transform'],
        'height':post_profile['height'],
        'width':post_profile['width']
    }
    with rio.MemoryFile(file_or_bytes=pre_img) as pre_memf,\
         rio.MemoryFile(file_or_bytes=post_img) as post_memf,\
         pre_memf.open() as pre_src,\
         post_memf.open() as pst_src,\
         WarpedVRT(src_dataset=pre_src,**vrt_profile) as pre_vrt,\
         WarpedVRT(src_dataset=pst_src,**vrt_profile) as pst_vrt:

        logger.debug(pre_vrt.profile)
        logger.debug(pst_vrt.profile)

        # rio_shutil.copy(pst_vrt,f'./tests/data/naga-post-vrt.tiff',driver='GTiff')

        with NamedTemporaryFile() as pre_memp,\
             NamedTemporaryFile() as pst_memp,\
             NamedTemporaryFile() as msk_memp,\
             NamedTemporaryFile() as dif_memp:
            
            pre_arr = pre_vrt.read()
            pst_arr = pst_vrt.read()
            logger.debug(pst_arr.shape)

            mask_memp = np.memmap(
                filename=msk_memp.name,dtype=pst_vrt.profile['dtype'],
                shape=pst_arr.shape
            )

            mask_memp[:] = pst_vrt.dataset_mask()
            mask_memp.flush()

            pre_memp_arr = np.memmap(
                filename=pre_memp.name,dtype=pre_vrt.profile['dtype'],
                shape=pre_arr.shape
            )
            pre_memp_arr[:] = pre_arr[:]
            pre_memp_arr.flush()
            pre_arr = None 

            pst_memp_arr = np.memmap(
                filename=pst_memp.name,dtype=pst_vrt.profile['dtype'],
                shape=pst_arr.shape
            )
            pst_memp_arr[:] = pst_arr[:]
            pst_memp_arr.flush()
            pst_arr = None
            logger.debug(pst_memp_arr.shape)

            diff_memp_arr = np.memmap(
                filename=dif_memp.name,dtype=pst_vrt.profile['dtype'],
                shape=pst_memp_arr.shape
            )

            diff_memp_arr[:] = pst_memp_arr - pre_memp_arr
            diff_memp_arr.flush()

            threshold = np.where(diff_memp_arr<-0.1,1,0)

            maj_arr = majority(image=threshold[0],footprint=square(width=5))

            # derive most variables from post img
            # profile, but change nodata to 0
            maj_filt_profile = DefaultGTiffProfile(
                **post_profile
            )
            maj_filt_profile.update(nodata=0)
            maj_filt_profile.update(compress='DEFLATE')
            maj_filt_profile.update(dtype='uint8')

            filepath = os.path.join(
                OUTPUT_DIR,f'{dt.datetime.now().strftime("%Y%m%d%H%M%S")}-sentinel1b-{LOCATION}-{EVENT}-flood.tiff') 

            with rio.open(
                fp=filepath,mode='w',
                **maj_filt_profile
            ) as tmp_src:
                tmp_src.write(maj_arr,1)

                logger.info(f'Connecting to database')
                cnxn = sqlite3.connect(database=DB_PATH)
                cur = cnxn.cursor()

                cur.execute(f"""
                            INSERT INTO flood VALUES
                            ('{uuid4()}','sentinel1b','{filepath}','{dt.datetime.now().isoformat()}')
                            """)

                cnxn.commit()
                cnxn.close()

    return

if __name__=="__main__":
    logger = logging.getLogger(__name__)