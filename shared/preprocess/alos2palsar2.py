import rasterio as rio
import numpy as np
import logging
import otbApplication as otb
from rasterio.warp import (
    calculate_default_transform, reproject
    )
from tempfile import NamedTemporaryFile
from shared.utils import derive_minmax_coords

logger = logging.getLogger(__name__)

def calibrate_backscatter(band: np.ndarray):
    backscatter = 20 * np.log10(band) - 83.0

    return backscatter

def speckle_filtering(band: np.ndarray):
    input = band.astype(dtype='float64')

    app = otb.Registry.CreateApplication("Despeckle")
    app.SetImageFromNumpyArray('in',input)
    app.SetParameterString('filter','lee')
    app.SetParameterInt('filter.lee.rad',1)
    app.SetParameterInt('filter.lee.nblooks',1)
    app.Execute()

    filtered = app.GetImageAsNumpyArray('out')
    casted = filtered.astype(dtype='float64',copy=False)
    return casted

def main():

    return

if __name__=="__main__":
    main()