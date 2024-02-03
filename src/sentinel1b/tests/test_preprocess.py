from ..preprocess import (
    geocode_img,
    init_datasets
)
import os
import pytest
import logging
import rasterio as rio
import shared.utils as utils
import xml.etree.ElementTree as ET
import elevation
from shapely.geometry import box

logger = logging.getLogger(__name__)

def test_geocode(sentinel1b_post_fp):

    geocoded = geocode_img(sentinel1b_post_fp)

    assert False


def test_init_ds(sentinel1b_post_fp,ph_pov_inc_2020,ph_90m_dem):

    datasets = init_datasets(
        safe_fp=sentinel1b_post_fp, bounds_fp=ph_pov_inc_2020,
        dem_fp=ph_90m_dem
    )

    assert False