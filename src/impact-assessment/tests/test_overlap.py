import os
import pytest
import json
import logging
import rasterio as rio
import numpy as np

from zipfile import ZipFile
from tempfile import TemporaryDirectory
from rasterio.windows import Window, from_bounds
from rasterio.transform import from_bounds as transform_from_bounds
from rasterio.transform import xy, rowcol
from tempfile import NamedTemporaryFile
from .. import overlap as op
from .. import app
from shared.utils import (
    convert_to_raster,
    logical_combination,
    raster_to_features
)
from geopandas import GeoDataFrame
from pyproj.crs import CRS

logger = logging.getLogger(__name__)

def test_init_data(flood_fp, ph_municity_bounds, ph_pov_inc_2020):

    with ZipFile(file=flood_fp) as archive,\
         TemporaryDirectory() as tmp_dir:
        logger.debug(os.getcwd())
        extract_fp = archive.extract(member='filtered.tiff',path=tmp_dir)
        _ = op.initialize_data(
            flood_fpath=extract_fp, admin_bnds_fpath=ph_municity_bounds,
            pov_inc_fpath=ph_pov_inc_2020
        )
    
        assert False
        # assert type(flood) is GeoDataFrame and type(bounds) is GeoDataFrame

def test_overlap_analysis(data):

    flood_ds, bounds_ds, _ = data

    result = op.overlap_analysis(
        flood=flood_ds, bounds=bounds_ds
    )

    with open(file='./tests/data/overlapped.json', mode='w') as f:
        f.write(json.dumps(result.__geo_interface__))
    assert False

def test_pov_incidence_reclass(data):
    
    _, bounds, pov_inc = data
    
    result = op.poverty_incidence_reclassify(pov_data=pov_inc)

    
    with open(file='./tests/data/pov_reclassed.json', mode='w') as f:
        f.write(json.dumps(result.__geo_interface__))
    assert False

def test_rasterize(overlap_bounds):

    result = convert_to_raster(
        feature_collection=overlap_bounds, crs=CRS.from_epsg(32651),
        resolution=30)

    assert False

def test_logical_recomb(input_for_combination):

    flooded, pov_inc = input_for_combination

    with rio.MemoryFile(file_or_bytes=flooded) as mem_f,\
    rio.MemoryFile(file_or_bytes=pov_inc) as mem_p,\
    mem_f.open() as src_f,\
    mem_p.open() as src_p:
        logger.debug(src_f.profile)
        logger.debug(src_p.profile)

        # create window based on bounds of smaller
        # dataset (flooded) but with transform
        # of larger dataset (poverty index)
        bounds = src_f.bounds
        window = from_bounds(
            left=bounds[0],bottom=bounds[1],right=bounds[2],top=bounds[3],
            transform=src_p.transform
        )

        window_transform = src_p.window_transform(window)
        pov_array = src_p.read(window=window,indexes=1,boundless=True)
        flood_array = src_f.read(indexes=1,boundless=True,fill_value=0)
        pov_array[flood_array==0] = 0

        result = logical_combination(array_1=pov_array,array_2=flood_array)
        logger.debug(result)

        profile = src_f.profile
        profile['transform'] = window_transform

        with rio.open(
            fp='./tests/data/logical_comb.tiff',mode='w',**profile
        ) as t:
            t.write(result,1)
    assert False

def test_execute(
        flood_fp, ph_municity_bounds,
        ph_pov_inc_2020
):

    result = app.execute(
        flood_fpath=flood_fp, bounds_fpath=ph_municity_bounds,
        pov_inc_fpath=ph_pov_inc_2020
    )

    assert False

def test_vectorize(flood_ds):
    ds, profile = flood_ds

    vectorized = raster_to_features(
        src_ds=ds,transform=profile['transform']
        )

    with open(file=f'./tests/data/vectorized.json',mode='w') as ds:
        ds.write(json.dumps(vectorized))

    assert False
