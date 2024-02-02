import os
import pytest

@pytest.fixture
def sentinel1b_pre_fp():

    return

@pytest.fixture
def sentinel1b_post_fp():

    fp = f'./tests/data/SENTINEL1/S1B_IW_GRDH_1SDV_20201113T095857_20201113T095922_024245_02E184_B28B.SAFE'

    return fp
   
@pytest.fixture
def sentinel1b_post_fp_measurement(sentinel1b_post_fp):

    fp = os.path.join(sentinel1b_post_fp,'measurement/s1b-iw-grd-vh-20201113t095857-20201113t095922-024245-02e184-002.tiff')

    return fp

@pytest.fixture
def sentinel1b_post_fp_manifest(sentinel1b_post_fp):

    fp = os.path.join(sentinel1b_post_fp,'manifest.safe')

    return fp

@pytest.fixture
def ph_pov_inc_2020():

    return f'./tests/data/National_PopAHS_PSA_2020.shp'

@pytest.fixture
def ph_90m_dem():

    return f'zip+file://./tests/data/N00E120.zip'