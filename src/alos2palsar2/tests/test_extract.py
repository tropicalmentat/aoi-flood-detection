import src.extract as ex

def test_extract(alos2palsar2_fp):

    result = ex.extract(img_fp=alos2palsar2_fp)

    assert False