import extract as le

def test_extract(landsat_b3_fp,
                 landsat_b5_fp,
                 landsat_mtl_fp):

    ndwi = le.extract(band3_fp=landsat_b3_fp,
                      band5_fp=landsat_b5_fp,
                      mtl_fp=landsat_mtl_fp)

    assert False