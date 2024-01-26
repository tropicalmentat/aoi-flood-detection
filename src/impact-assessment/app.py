from . import overlap as op
from shared.utils import(
    convert_to_raster,
    logical_combination
)
from rasterio.vrt import WarpedVRT
import logging
import json
import rasterio as rio

logger = logging.getLogger(__name__)

def execute(flood_fpath, bounds_fpath, pov_inc_fpath): 

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
    rasterized_povinc, pi_profile = convert_to_raster(
        feature_collection=reclassed_pi_fc, resolution=30,
        crs=flood_profile['crs']
    )
    rasterized_bounds, bnds_profile = convert_to_raster(
        feature_collection=overlap_fc, resolution=30,
        crs=flood_profile['crs']
    )

    # TODO: Create vrt profile from flood raster
    vrt_profile = {

    }
    # TODO: align rasterized bounds
    pi_array = None
    overlap_array = None
    with rio.MemoryFile(file_or_bytes=rasterized_povinc) as pi_mem,\
         rio.MemoryFile(file_or_bytes=rasterized_bounds) as bnds_mem,\
         pi_mem.open(**pi_profile) as pi_src,\
         bnds_mem.open(**bnds_profile) as bnds_src,\
         WarpedVRT(src_dataset=pi_src, **flood_profile) as pi_vrt,\
         WarpedVRT(src_dataset=bnds_src, **flood_profile) as bnds_vrt:
            logger.debug(pi_vrt.profile)
            logger.debug(bnds_vrt.profile)
            pi_array = pi_vrt.read()
            overlap_array = bnds_vrt.read()

    # run logical combination of rasterized overlap results and pov inc
    log_com = logical_combination(array_1=pi_array,array_2=overlap_array)
# 
    with rio.open(
        fp='./tests/data/flood-impact.tiff',mode='w', **bnds_profile
    ) as src:
        src.write(log_com,1)
# 
    return