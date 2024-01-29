from . import overlap as op
from rasterio.vrt import WarpedVRT
from rasterio.profiles import DefaultGTiffProfile
from tempfile import NamedTemporaryFile

import rasterio.windows as win
import shared.utils as utils
import logging
import json
import numpy as np
import rasterio as rio

logger = logging.getLogger(__name__)

def execute(
          flood_fpath, bounds_fpath, pov_inc_fpath, 
          resolution=500)

    # DATA INITIALIZATION
    # check if coordinate systems are the same
    # get bounding box of flood data
    # get intersect of poverty incidence data
    # get intersect of admin boundary data
    bounds, pov_inc, flood, flood_profile = op.initialize_data(
        flood_fpath=flood_fpath, admin_bnds_fpath=bounds_fpath,
        pov_inc_fpath= pov_inc_fpath
    )
    logger.debug(flood_profile)

    # run overlap analysis of flood and admin bounds
    overlap = op.overlap_analysis(flood=flood, bounds=bounds) 

    # run reclassification of pov inc and overlap results
    reclassed_povinc = op.poverty_incidence_reclassify(
        pov_data=pov_inc
    )

    reclassed_pi_fc = json.loads(reclassed_povinc.to_json())
    overlap_fc = json.loads(overlap.to_json())
    
    with open(file=f'./tests/data/reclassed_pi.json',mode='w') as tmp_rpi:
        tmp_rpi.write(json.dumps(reclassed_pi_fc))
    
    with open(file=f'./tests/data/reclassed_overlap.json',mode='w') as tmp_rov:
        tmp_rov.write(json.dumps(overlap_fc))

    # rasterize reclassified pov inc and overlap results
    # with a resolution of 30 x 30 meters
    # and crs of that of the flood raster
    rasterized_povinc, pi_profile = utils.convert_to_raster(
        feature_collection=reclassed_pi_fc, resolution=resolution,
        crs=flood_profile['crs']
    )
    rasterized_bounds, bnds_profile = utils.convert_to_raster(
        feature_collection=overlap_fc, resolution=resolution,
        crs=flood_profile['crs']
    )
    with open(file=f'./tests/data/rasterized-pi.tiff',mode='wb') as tmppi:
        tmppi.write(rasterized_povinc)

    with open(file=f'./tests/data/rasterized-overlap.tiff',mode='wb') as tmpov:
        tmpov.write(rasterized_bounds)
    
    # Form profile that has the bounds of the input flood data
    # and the resolution of the rasterized data
    out_transform = 

    logger.info('Starting logical combination')
    with rio.MemoryFile(file_or_bytes=rasterized_povinc) as pi_mem,\
         rio.MemoryFile(file_or_bytes=rasterized_bounds) as bnds_mem,\
         pi_mem.open(**pi_profile) as pi_src,\
         bnds_mem.open(**bnds_profile) as bnds_src,\
         WarpedVRT(src_dataset=pi_src, **pi_profile) as pi_vrt,\
         WarpedVRT(src_dataset=bnds_src, **pi_profile) as bnds_vrt,\
         NamedTemporaryFile() as tmp:
            log_com_array = np.memmap(
                filename=tmp.name,shape=(pi_profile['height'],pi_profile['width'])
            )
            logger.debug(pi_vrt.profile)
            logger.debug(bnds_vrt.profile)

            pi_array = pi_vrt.read()
            overlap_array = bnds_vrt.read()
            combined = utils.logical_combination(
                array_1=pi_array,array_2=overlap_array
            )
            try:
                log_com_array[:] = combined[:]
                log_com_array.flush()
            except ValueError as e:
                logger.warning(f'Axis are swapped')
                transposed = np.transpose(combined) 
                log_com_array[:] = transposed[:]
                log_com_array.flush()
            with rio.open(
                fp='./tests/data/flood-impact.tiff',mode='w', **pi_profile
            ) as src:
                src.write(log_com_array,1)

    return