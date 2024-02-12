import pytest
import json
import geopandas as gpd
import logging
import rasterio as rio
from zipfile import ZipFile

logger = logging.getLogger(__name__)

@pytest.fixture
def flood_fp():

    # return f'./tests/data/overlapped.json.zip'
    # return f'./tests/data/mnl_flood.json'
    # return f'./tests/data/filtered.tiff.zip'
    return f'./tests/data/cagayan-maj-filtered.tiff.zip'

@pytest.fixture
def flood_ds(flood_fp):

    flood_array = None
    profile = None
    with ZipFile(file=flood_fp,mode='r') as archive:
        logger.debug(archive.namelist())
        img_bin = archive.read(name='filtered.tiff')
        with rio.MemoryFile(file_or_bytes=img_bin) as mem_src:
            flood_ds = mem_src.open()
            profile = flood_ds.profile
            flood_array = flood_ds.read()
    return flood_array, profile

@pytest.fixture
def ph_municity_bounds():

    # return f'./tests/data/National_AB3_NAMRIA_2022_ncr-laguna.shp'
    return f'./tests/data/National_AB3_NAMRIA_2022.shp'

@pytest.fixture
def ph_pov_inc_2020():

    # return f'./tests/data/National_PopAHS_PSA_2020_ncr-laguna.shp'
    return f'./tests/data/National_PopAHS_PSA_2020.shp'

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

@pytest.fixture
def pov_inc_reclassed():

    fp = f'./tests/data/pov_reclassed.json.zip'

    with ZipFile(file=fp) as archive:
        data = json.loads(archive.read(name=f'pov_reclassed.json'))
        return data

@pytest.fixture
def input_for_combination():

    fp = f'./tests/data/logical_comb_input.zip'

    with ZipFile(file=fp) as archive:
        logger.debug(archive.namelist())
        flooded = archive.read(name='flood_overlap.tiff')
        pov_inc = archive.read(name='pov_inc_raster.tiff')

        return flooded, pov_inc