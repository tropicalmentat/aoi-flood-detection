import pytest
import json
import geopandas as gpd

@pytest.fixture
def flood_fp():

    return f'./tests/data/mnl_flood.json'

@pytest.fixture
def ph_municity_bounds():

    return f'./tests/data/National_AB3_NAMRIA_2022_ncr-laguna.shp'

@pytest.fixture
def data(flood_fp, ph_municity_bounds):

    flood_df = None
    flood_crs = None
    bounds_df = None
    with open(flood_fp,mode='r') as flood_src:
        flood_fc = json.loads(flood_src.read())
        flood_crs = flood_fc['crs']
        flood_df = gpd.GeoDataFrame.from_features(flood_fc)
    
    bounds_df = gpd.GeoDataFrame.from_file(ph_municity_bounds)
    
    flood_df.set_crs(flood_crs,inplace=True)

    return flood_df, bounds_df