import rasterio as rio
from rasterio.vrt import WarpedVRT
from shared.utils import (
    build_alos2palsar2_metadata, 
    derive_minmax_coords,
    get_window_offsets,
    window_to_array,
    get_bounds_intersect,
    project_image
)
import logging

logger = logging.getLogger(__name__)
logging.getLogger('rasterio').setLevel(logging.CRITICAL)

def test_build_metadata(alos2palsar2_summary_fp):

    metadata = build_alos2palsar2_metadata(metadata_fp=alos2palsar2_summary_fp)

    assert False

def test_derive_minmax_coords(alos2palsar2_band):
    _,profile = alos2palsar2_band

    bounds = derive_minmax_coords(profile=profile)
    logger.debug(bounds)

    assert False

def test_window_img_read(alos2palsar2_pre_img):

    src = rio.MemoryFile(alos2palsar2_pre_img).open()

    offsets, cols, rows = get_window_offsets(img=alos2palsar2_pre_img)

    assert len(offsets)==len(cols)*len(rows)

    count = 0
    for pair in offsets:
        
        if pair[0] == cols[-1] or pair[1] == rows[-1]:
            array, transform, slice = window_to_array(
                src=src, offset_pair=pair)
            count+=1
            logger.debug(array.shape)
        else:
            array, transform, slice = window_to_array(
                src=src, offset_pair=pair,edge=False
            )
            logger.debug(array.shape)
            count+=1
        # logger.debug(array.shape) 
    logger.debug(count)
    assert count == len(offsets)
    
def test_img_bounds_intersection(
        alos2palsar2_pre_img, alos2palsar2_post_img
        ):
    
    intersect_window =  get_bounds_intersect(
        pre_img=alos2palsar2_pre_img, post_img=alos2palsar2_post_img,
        dst_crs=rio.CRS.from_epsg(32651)
    )
    logger.debug(intersect_window.height)
    logger.debug(intersect_window.width)
    
    offsets, cols, rows = get_window_offsets(img=alos2palsar2_pre_img)

    count = 0
    for pair in offsets:
        
        if pair[0] == cols[-1] or pair[1] == rows[-1]:
            array, transform, slice = window_to_array(
                img=alos2palsar2_pre_img, offset_pair=pair)
            count+=1
        else:
            array, transform, slice = window_to_array(
                img=alos2palsar2_pre_img, offset_pair=pair,edge=False
            )
            count+=1

    assert False

def test_project_img(alos2palsar2_pre_band):

    band, profile, bounds = alos2palsar2_pre_band
    logger.debug(band.shape)
    logger.debug(profile)
    logger.debug(bounds)

    projected = project_image(
        band=band,bounds=bounds,src_profile=profile,src_crs=profile.get('crs'),
        dst_crs=rio.CRS.from_epsg(32651)
    )
    assert False

def test_warpedvrt(alos2palsar2_post_fp):

    with rio.open(
        fp=alos2palsar2_post_fp
    ) as src,\
         WarpedVRT(src_dataset=src,src_crs=rio.CRS.from_epsg(32651),crs=rio.CRS.from_epsg(4326)) as wrp:
        logger.debug(wrp.profile) 

    assert False