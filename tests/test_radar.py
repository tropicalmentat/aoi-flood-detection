import utils

def test_load_img(pre_goni_cv_opt):
    
    img = utils.load_band(fpath=pre_goni_cv_opt)

    assert False