from . import overlap as op
from rasterio.vrt import WarpedVRT

import rasterio.windows as win
import shared.utils as utils
import logging
import json
import rasterio as rio

logger = logging.getLogger(__name__)

def execute(flood_fpath, bounds_fpath, pov_inc_fpath): 

    # Retrieve window offsets that will be used
    # for windowed logical recombination
    flood_img = utils.load_image(fpath=flood_fpath)
    offsets, col_offsets, row_offsets = utils.get_window_offsets(
          img=flood_img
    )

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

    # rasterize reclassified pov inc and overlap results
    # with a resolution of 30 x 30 meters
    # and crs of that of the flood raster
    rasterized_povinc, pi_profile = utils.convert_to_raster(
        feature_collection=reclassed_pi_fc, resolution=30,
        crs=flood_profile['crs']
    )
    rasterized_bounds, bnds_profile = utils.convert_to_raster(
        feature_collection=overlap_fc, resolution=30,
        crs=flood_profile['crs']
    )

    logger.info('Starting logical combination')
    with rio.MemoryFile(file_or_bytes=rasterized_povinc) as pi_mem,\
         rio.MemoryFile(file_or_bytes=rasterized_bounds) as bnds_mem,\
         pi_mem.open(**pi_profile) as pi_src,\
         bnds_mem.open(**bnds_profile) as bnds_src,\
         WarpedVRT(src_dataset=pi_src, **flood_profile) as pi_vrt,\
         WarpedVRT(src_dataset=bnds_src, **flood_profile) as bnds_vrt:
            logger.debug(pi_vrt.profile)
            logger.debug(bnds_vrt.profile)

            for pair in offsets:
                if pair[0] == col_offsets[-1] or pair[1] == row_offsets[-1]:
                    window = win.Window.from_slices(
                        cols=(pair[0],flood_profile['width']), rows=(pair[1],flood_profile['height'])
                        )
                    pi_array = pi_vrt.read(window=window)
                    overlap_array = bnds_vrt.read(window=window)
                    log_com = utils.logical_combination(
                         array_1=pi_array,array_2=overlap_array
                         )
                    logger.debug(log_com)
                else:
                    window = win.Window(
                        col_off=pair[0],row_off=pair[1],
                        width=1024, height=1024
                    )
                    pi_array = pi_vrt.read(window=window)
                    overlap_array = bnds_vrt.read(window=window)
                    log_com = utils.logical_combination(
                         array_1=pi_array,array_2=overlap_array
                         )
    # TODO window logical combination
    # run logical combination of rasterized overlap results and pov inc
    # log_com = logical_combination(array_1=pi_array,array_2=overlap_array)
# 
    # with rio.open(
        # fp='./tests/data/flood-impact.tiff',mode='w', **bnds_profile
    # ) as src:
        # src.write(log_com,1)
# 
    return