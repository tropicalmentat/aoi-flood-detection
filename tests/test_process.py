from process_optical import load_img
import logging

logger = logging.getLogger(__name__)

def test_load_img(pre_goni_cv_opt):

    img = load_img(pre_goni_cv_opt)    

    assert False