import landsat_extract as le

def test_prepare(landsat_b3_fp,
                 landsat_b5_fp,
                 landsat_mtl_fp):

    prepared = le.prepare(band3_fp=landsat_b3_fp,
                          band5_fp=landsat_b5_fp,
                          mtl_fp=landsat_mtl_fp)


    assert False