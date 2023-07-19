import rasterio as rio
import logging
import numpy as np
from math import pi
from numpy.ma import nomask

logger = logging.getLogger(__name__)

def dn_to_radiance(array: np.ndarray):
    # gain and bias are from the 
    # image .MTL file in the RADIOMETRIC
    # RESCALING segment
    # gain = RADIANCE_MULT_<BAND NUMBER>
    # bias = RADIANCE_ADD_<BAND NUMBER>
    gain = 0.012059
    bias = -60.29402
    
    # TODO: apply mask to this operation
    radiance_array = gain*array + bias

    return radiance_array

def radiance_to_reflectance(array: np.ndarray,band: int, metadata: dict):
    # OLI top-of-atmosphere reflectance
    mult_scaling_factor = metadata[f'RADIANCE_MULT_BAND_{str(band)}']
    add_scaling_factor = metadata[f'RADIANCE_ADD_BAND_{str(band)}']

    toa_reflectance = (mult_scaling_factor * array) + add_scaling_factor

    return toa_reflectance

def preprocess_landsat(img: bytes):

    # read image and extract profile

    return

def main():
    
    return

if __name__=="__main__":
    main()