from ..preprocess import (
    geocode_img,
    init_datasets
)
from ..extract import extract
import os
import pytest
import logging
import rasterio as rio
import shared.utils as utils
import xml.etree.ElementTree as ET
import elevation
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

def test_geocode(sentinel1b_post_fp):

    geocoded = geocode_img(sentinel1b_post_fp)

    assert False


def test_init_ds(sentinel1b_post_fp,ph_pov_inc_2020,ph_90m_dem):

    with NamedTemporaryFile() as tmp:
        arr, profile = init_datasets(
            safe_fp=sentinel1b_post_fp, bounds_fp=ph_pov_inc_2020,
            dem_fp=ph_90m_dem,memmap_fn=tmp.name
        )
        with rio.open(fp=f'./tests/data/sentinel1b-despeckled.tiff',mode='w',**profile) as src:
            src.write(arr,indexes=1)

    assert False

def test_flood_extract(sentinel1b_pre_fp,sentinel1b_post_fp,ph_pov_inc_2020,ph_90m_dem):

    result = extract(
        pre_safe_fp=sentinel1b_pre_fp,post_safe_fp=sentinel1b_post_fp,
        bounds_fp=ph_pov_inc_2020,dem_fp=ph_90m_dem
    )

    assert False