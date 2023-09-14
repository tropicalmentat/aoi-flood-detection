from shared.preprocess.sentinel1b import (
    geocode_img
)
import pytest
import logging

logger = logging.getLogger(__name__)

def test_geocode(sentinel1b_post_fp):

    geocoded = geocode_img(sentinel1b_post_fp)

    assert False