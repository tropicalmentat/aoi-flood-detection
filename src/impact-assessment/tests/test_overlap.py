import pytest
from .. import overlap as op
from geopandas import GeoDataFrame

def test_init_data(flood_fp, ph_municity_bounds):

    flood, bounds = op.initialize_data(
        flood_fpath=flood_fp, bounds_fpath=ph_municity_bounds
    )

    assert type(flood) is GeoDataFrame and type(bounds) is GeoDataFrame

def test_overlap(data):

    flood_ds, bounds_ds = data

    result = op.overlap_analysis(
        flood=flood_ds, bounds=bounds_ds
    )

    assert False
