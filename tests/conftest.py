import pytest

@pytest.fixture
def pre_goni_cv_opt():
    # optical img for typhoon goni
    # for cagayan valley pre typhoon
    fp = f'./tests/data/s1b-iw-grd-vh-20200914t095832-20200914t095857-023370-02c637-002.tiff'

    return fp