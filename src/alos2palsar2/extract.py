import os
import numpy as np
import shared.utils as utils
import rasterio as rio
import logging

from shared.preprocess.radar import (
    despeckle
)
from tempfile import NamedTemporaryFile
from skimage.morphology import square
from skimage.filters.rank import majority
from rasterio.profiles import DefaultGTiffProfile
from rasterio.vrt import WarpedVRT

logger = logging.getLogger(__name__)

def get_pre_post_imgs(indir):

    logger.debug(indir)
    pre_fn = None
    post_fn = None

    return os.path.join(indir,pre_fn), os.path.join(indir,post_fn)

def get_preprocessed(
                     img_bin: bytes = None,
                     block_size:int=1024,
                     intersect_window = None,
                     dst_crs = None
                     ):

    calibrated = None
    profile = None

    with NamedTemporaryFile() as tmp_bs, \
         NamedTemporaryFile() as tmp_ds, \
         rio.MemoryFile(file_or_bytes=img_bin) as mem, \
         mem.open() as src, \
         WarpedVRT(src_dataset=src,src_crs=dst_crs) as wrp:

        profile = wrp.profile
        logger.debug(profile)

        calibrated = np.memmap(
            filename=tmp_bs.name, dtype=np.float16,
            shape=(int(profile['height'] if intersect_window is None else intersect_window.height),
                   int(profile['width'] if intersect_window is None else intersect_window.width))
        )
        profile.update(dtype=calibrated.dtype)

        despeckled = np.memmap(
            filename=tmp_ds.name, dtype=np.float16,
            shape=(profile.get('height'),profile.get('width'))
        )

        offsets, col_offs, row_offs = utils.get_window_offsets(
            img=img_bin, block_size=block_size
        )
    
        slices = []
        for i,pair in enumerate(offsets,start=1):
            logger.info(f'Calibrate window {i}')
            array = None
            transform = None
            if pair[0] == col_offs[-1] or pair[1] == row_offs[-1]:
                array, transform, slice = utils.window_to_array(
                    src=wrp, offset_pair=pair,block_size=block_size,
                    intersect_window=intersect_window
                )
                calibrated[slice] = 20 * np.log10(array) - 83.0
                slices.append(slice)
            else:
                array, transform, slice = utils.window_to_array(
                    src=wrp, offset_pair=pair,block_size=block_size,
                    edge=False, intersect_window=intersect_window
                )
                calibrated[slice] = 20 * np.log10(array) - 83.0
                slices.append(slice)

        for i,slice in enumerate(slices,start=1):
            logger.info(f'Despeckle window {i}')
            # TODO: Despeckle with buffered slice
            despeckled[slice] = despeckle(band=calibrated[slice])
            calibrated[slice] = np.nan_to_num(despeckled[slice],nan=-9999.0,posinf=-9999.0,neginf=-9999.0)
        
    # TODO: remove 3rd tuple value 
    return calibrated, profile, None 

def extract(pre_fp:str, post_fp:str):

    # TODO add image sorter
    # TODO user WarpedVRT at the preprocessing stage to automatically reproject
    # image data into the destination projection
    pre_img_bin = utils.load_image(fpath=pre_fp)
    post_img_bin = utils.load_image(fpath=post_fp)

    # align bounds of pre and post-disaster
    # images using intersecting window
    # NOTE FORCE USE OF EPSG 32651 FOR ALOS2 PALSAR2
    # IMAGES
    intersect_window = utils.get_bounds_intersect(
        pre_img=pre_img_bin, post_img=post_img_bin, dst_crs=rio.CRS.from_epsg(32651)
        )

    pre,pre_profile,pre_bounds = get_preprocessed(
        img_bin=pre_img_bin, block_size=2048, intersect_window=intersect_window,
        dst_crs=rio.CRS.from_epsg(32651)
        )

    post,post_profile,post_bounds = get_preprocessed(
        img_bin=post_img_bin, block_size=2048, intersect_window=intersect_window,
        dst_crs=rio.CRS.from_epsg(32651)
        )

    logger.debug(pre.shape)
    logger.debug(post.shape)

    diff = np.ma.masked_equal(
        post,value=pre_profile['nodata']) - np.ma.masked_equal(pre,value=pre_profile['nodata'])
    
    with rio.open(fp=f'./tests/data/pampanga-diff.tiff',mode='w',**post_profile) as tmp_dif:
        tmp_dif.write(diff,1)

    logger.info(f'Applying threshold')

    threshold = np.ma.where(diff<-3,1,0)

    logger.info(f'Applying majority filter')

    # use post img profile and set nodata to 0
    maj_filt_profile = DefaultGTiffProfile(
        **post_profile
    )
    maj_filt_profile.update(nodata=0)
    maj_filt_profile.update(dtype='uint8')
    maj_filt_profile.update(compress='DEFLATE')

    maj_filt_arr = majority(image=threshold[0],footprint=square(width=5))

    # TODO SAVE THIS TO A FOLDER WHERE THE NEXT STAGE CAN PICK UP
    with rio.open(
        fp=f'./tests/data/filtered.tiff',mode='w',
        **maj_filt_profile
    ) as tmp:
        tmp.write(maj_filt_arr,1)
    