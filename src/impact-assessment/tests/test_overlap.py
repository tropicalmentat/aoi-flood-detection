import pytest
import json
import logging
from .. import overlap as op
from shared.utils import convert_to_raster
from geopandas import GeoDataFrame
from pyproj.crs import CRS

logger = logging.getLogger(__name__)

def test_init_data(flood_fp, ph_municity_bounds):

    flood, bounds = op.initialize_data(
        flood_fpath=flood_fp, bounds_fpath=ph_municity_bounds
    )

    assert type(flood) is GeoDataFrame and type(bounds) is GeoDataFrame

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

    result = convert_to_raster(feature_collection=overlap_bounds, crs=CRS.from_epsg(32651))

    assert False