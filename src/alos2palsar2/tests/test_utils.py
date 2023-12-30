from shared.utils import (
    build_alos2palsar2_metadata, 
    derive_minmax_coords,
    get_window_offsets,
    window_to_array
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

    offsets, cols, rows = get_window_offsets(img=alos2palsar2_pre_img)

    count = 0
    for pair in offsets:
        
        array = None
        transform = None
        if pair[0] == cols[-1] or pair[1] == rows[-1]:
            array, transform = window_to_array(
                img=alos2palsar2_pre_img, offset_pair=pair)
            count+=1
        else:
            array, transform = window_to_array(
                img=alos2palsar2_pre_img, offset_pair=pair
            )
            count+=1
    
    logger.debug(count)
    assert count == len(offsets)