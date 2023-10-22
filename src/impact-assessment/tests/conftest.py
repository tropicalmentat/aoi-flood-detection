import pytest
import json
import geopandas as gpd
from zipfile import ZipFile

@pytest.fixture
def flood_fp():

    return f'./tests/data/mnl_flood.json'

@pytest.fixture
def ph_municity_bounds():

    return f'./tests/data/National_AB3_NAMRIA_2022_ncr-laguna.shp'

@pytest.fixture
def ph_pov_inc_2020():

    return f'./tests/data/National_PopAHS_PSA_2020_ncr-laguna.shp'

@pytest.fixture
def data(flood_fp, ph_municity_bounds, ph_pov_inc_2020):

    flood_df = None
    flood_crs = None
    bounds_df = None
    with open(flood_fp,mode='r') as flood_src:
        flood_fc = json.loads(flood_src.read())
        flood_crs = flood_fc['crs']
        flood_df = gpd.GeoDataFrame.from_features(flood_fc)
    
    bounds_df = gpd.GeoDataFrame.from_file(ph_municity_bounds)

    pov_inc_df = gpd.GeoDataFrame.from_file(ph_pov_inc_2020)
    
    flood_df.set_crs(flood_crs,inplace=True)

    return flood_df, bounds_df, pov_inc_df

@pytest.fixture
def overlap_bounds():

    fp = f'./tests/data/overlapped.json.zip'

    with ZipFile(file=fp) as archive:
        data = json.loads(archive.read(name=f'overlapped.json'))
        return data