from . import overlap as op
from rasterio.vrt import WarpedVRT
from rasterio.transform import from_bounds
from rasterio.profiles import DefaultGTiffProfile
from rasterio.windows import from_bounds as window_from_bounds
from tempfile import NamedTemporaryFile

import affine
import rasterio.windows as win
import shared.utils as utils
import logging
import json
import numpy as np
import rasterio as rio

logger = logging.getLogger(__name__)

def execute(
          flood_fpath, bounds_fpath, pov_inc_fpath, 
          resolution=500):

    # DATA INITIALIZATION
    # check if coordinate systems are the same
    # get bounding box of flood data
    # get intersect of poverty incidence data
    # get intersect of admin boundary data
    bounds, pov_inc, flood, flood_profile = op.initialize_data(
        flood_fpath=flood_fpath, admin_bnds_fpath=bounds_fpath,
        pov_inc_fpath= pov_inc_fpath
    )
    logger.debug(flood.total_bounds)
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
    # use crs of that of the flood raster
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
    
    # Init raster profile that has the 
    # bounds of the input flood data
    # and the resolution of the rasterized data
    left, bottom, right, top = flood.total_bounds
    out_width = right - left
    out_height = top - bottom
    logger.debug(out_width)
    logger.debug(out_height)
    out_cols = round(out_width/resolution)
    out_rows = round(out_height/resolution)
    out_shape = (out_rows, out_cols)
    out_transform = from_bounds(
        west=left,south=bottom,east=right,north=top,
        width=out_cols,height=out_rows
    )
    out_profile = DefaultGTiffProfile(
        crs=flood_profile['crs'], transform=out_transform,
        height=round(out_rows), width=round(out_cols), count=1
    )
    window = window_from_bounds(
        left=left, bottom=bottom,right=right,top=top,
        transform=out_transform
    )

    logger.debug(out_profile)

    logger.info('Starting logical combination')
    # TODO Fix normalization of datasets within common bounding box
    with rio.MemoryFile(file_or_bytes=rasterized_povinc) as pi_mem,\
         rio.MemoryFile(file_or_bytes=rasterized_bounds) as bnds_mem,\
         pi_mem.open() as pi_src,\
         bnds_mem.open() as bnds_src,\
         WarpedVRT(pi_src,**out_profile) as pi_vrt,\
         WarpedVRT(bnds_src,**out_profile) as ov_vrt,\
         NamedTemporaryFile() as tmp:
            logging.debug(pi_vrt.profile)
            logging.debug(ov_vrt.profile)
            log_com_array = np.memmap(
                filename=tmp.name,shape=out_shape
            )
            pi_array = pi_vrt.read(indexes=1)
            overlap_array = ov_vrt.read(indexes=1)
            combined = utils.logical_combination(
                array_1=overlap_array,array_2=pi_array
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
                fp=f'./tests/data/windowed-pi.tiff',mode='w', **out_profile
            ) as win_pi:
                win_pi.write(pi_array,1)
            with rio.open(
                fp=f'./tests/data/windowed-overlap.tiff',mode='w', **out_profile
            ) as win_ov:
                win_ov.write(overlap_array,1)
            with rio.open(
                fp='./tests/data/flood-impact.tiff',mode='w', **out_profile
            ) as src:
                src.write(log_com_array,1)

    return