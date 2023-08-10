from shared.utils import (
    build_alos2palsar2_metadata, derive_minmax_coords
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