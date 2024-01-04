import src.extract as ex
import logging
from json import loads, dumps
from zipfile import ZipFile
from rasterio.crs import CRS
from shared.utils import project_coordinates

logger = logging.getLogger(__name__)

def test_preprocessing(alos2palsar2_pre_fp,alos2palsar2_pre_img):

    preprocessed = ex.get_preprocessed(
        img_fp=alos2palsar2_pre_fp,img_bin=alos2palsar2_pre_img,block_size=2048
    )

    assert False

def test_extract_flood(alos2palsar2_pre_fp,alos2palsar2_post_fp):

    result = ex.extract(
        pre_fp=alos2palsar2_pre_fp, post_fp=alos2palsar2_post_fp
        )

    assert False

def test_project_coordinates(flood_extract,alos2palsar2_post_band):
    _,profile,_ = alos2palsar2_post_band
    dst_crs = CRS.from_epsg(32651)
    with ZipFile(file=flood_extract) as archive:
        data = loads(
            archive.read(name='mm_flood.json'))

        projected = project_coordinates(
            feature_collection=data,src_crs=profile['crs'],dst_crs=dst_crs
            )
        
        with open(file=f'./tests/data/mnl_flood.json',mode='w') as s:
            s.write(dumps(projected))

    assert False