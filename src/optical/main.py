import os
import logging
from extract import (
    extract_flood,
    extract_true_color
)

from sys import stdout
from tarfile import TarFile
from tempfile import TemporaryDirectory


logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler(stdout)
logger.addHandler(console_handler)

sensor = os.environ.get("SENSOR")
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
                        for mbr in tar.getnames():
                            if '.xml' in mbr:
                                tar.extract(member=mbr,path=tmpdir)
            logger.debug(os.listdir(tmpdir))
        elif sensor=="sentinel2":
            pass

        return

if __name__=="__main__":
    main()