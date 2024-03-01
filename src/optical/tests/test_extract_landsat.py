import src.extract as le

def test_extract_flood(landsat_b3_fp,
                 landsat_b5_fp,
                 landsat_mtl_fp):

    ndwi = le.extract_flood(band3_fp=landsat_b3_fp,
                            band5_fp=landsat_b5_fp,
                            mtl_fp=landsat_mtl_fp)

    assert False

def test_extract_true_color(
    landsat_b2_fp, landsat_b3_fp, landsat_b4_fp
):

    true_color = le.extract_true_color(
        band4_fp=landsat_b4_fp, band3_fp=landsat_b3_fp,
        band2_fp=landsat_b2_fp, outdir=f'./tests/data/l8_true_color.tiff'
    )
    assert False