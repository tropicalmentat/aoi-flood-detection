import src.extract as ex

def test_extract(alos2palsar2_pre_fp,alos2palsar2_post_fp):

    result = ex.extract(pre_fp=alos2palsar2_pre_fp, post_fp=alos2palsar2_post_fp)

    assert False