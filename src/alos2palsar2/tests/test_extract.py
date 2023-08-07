import src.extract as ex

def test_extract(alos2_palsar2_fp):

    result = ex.extract(img_fp=alos2_palsar2_fp)

    assert False