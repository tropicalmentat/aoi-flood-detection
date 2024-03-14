import os
import logging
import xml.etree.ElementTree as ET

from extract import (
    extract_flood,
    extract_true_color
)
from sys import stdout
from tarfile import TarFile
from tempfile import TemporaryDirectory
from zipfile import ZipFile


logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

sensor = os.environ.get("SENSOR")
algo = os.environ.get("ALGORITHM")
input = os.environ.get("INPUT")
output = os.environ.get("OUTPUT")

def main():
    logger.debug(sensor)
    logger.debug(input)
    logger.debug(output)

    with TemporaryDirectory() as tmpdir:
        if sensor=="landsat8":
            for fn in os.listdir(input):
                if '.tar' in fn:
                    with TarFile(name=os.path.join(input,fn)) as tar:
                        mtl_xml = None
                        mtl_txt = None
                        for mbr in tar.getnames():
                            if '.xml' in mbr:
                                tar.extract(member=mbr,path=tmpdir)
                                mtl_xml = mbr
                            elif 'MTL.txt' in mbr:
                                tar.extract(member=mbr,path=tmpdir)
                                mtl_txt = mbr

                        tree = ET.parse(source=os.path.join(tmpdir,mtl_xml))
                        root = tree.getroot()
                        product_info = root.find(path='PRODUCT_CONTENTS')

                        if algo == "ndwi":
                            green_band_fn = product_info.find(path='FILE_NAME_BAND_3').text
                            nir_band_fn = product_info.find(path='FILE_NAME_BAND_5').text

                            tar.extract(member=green_band_fn,path=tmpdir)
                            tar.extract(member=nir_band_fn,path=tmpdir)

                            extract_flood(
                                green_band_fp=os.path.join(tmpdir,green_band_fn),
                                nir_band_fp=os.path.join(tmpdir,nir_band_fn),
                                mtl_fp=os.path.join(tmpdir,mtl_txt)
                            )
                        elif algo == "truecolor":
                            red_band_fn = product_info.find(path="FILE_NAME_BAND_4").text
                            green_band_fn = product_info.find(path="FILE_NAME_BAND_3").text
                            blue_band_fn = product_info.find(path="FILE_NAME_BAND_2").text

                            tar.extract(member=red_band_fn,path=tmpdir)
                            tar.extract(member=green_band_fn,path=tmpdir)
                            tar.extract(member=blue_band_fn,path=tmpdir)

                            extract_true_color(
                                red_band_fp=os.path.join(tmpdir,red_band_fn),
                                green_band_fp=os.path.join(tmpdir,green_band_fn),
                                blue_band_fp=os.path.join(tmpdir,blue_band_fn)
                            )
            
        elif sensor=="sentinel2":
            for fn in os.listdir(input):
                if '.zip' in fn:
                    with ZipFile(file=os.path.join(input,fn),mode='r') as archive:
                        red_band_fn = None
                        green_band_fn = None
                        blue_band_fn = None
                        for fn in archive.namelist():
                            # red band
                            if "B04.jp2" in fn:
                                logger.debug(fn)
                                archive.extract(member=fn,path=tmpdir)
                                red_band_fn = os.path.join(tmpdir,fn)
                            # green band
                            elif "B03.jp2" in fn:
                                logger.debug(fn)
                                archive.extract(member=fn,path=tmpdir)
                                green_band_fn = os.path.join(tmpdir,fn)
                            # blue band
                            elif "B02.jp2" in fn:
                                logger.debug(fn)
                                archive.extract(member=fn,path=tmpdir)
                                blue_band_fn = os.path.join(tmpdir,fn)
                        
                        extract_true_color(
                            red_band_fp=red_band_fn,
                            green_band_fp=green_band_fn,
                            blue_band_fp=blue_band_fn
                        )
        return

if __name__=="__main__":
    main()