from . import overlap as op
from shared.utils import(
    convert_to_raster,
    logical_combination
)
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
    bounds, pov_inc, flood, crs = op.initialize_data(
        flood_fpath=flood_fpath, admin_bnds_fpath=bounds_fpath,
        pov_inc_fpath= pov_inc_fpath
    )

    # run overlap analysis of flood and admin bounds
    overlap = op.overlap_analysis(flood=flood, bounds=bounds) 
    logger.debug(overlap)

    # run reclassification of pov inc and overlap results
    reclassed_povinc = op.poverty_incidence_reclassify(
        pov_data=pov_inc
    )
    logger.debug(reclassed_povinc)

    reclassed_pi_fc = json.loads(reclassed_povinc.to_json())
    overlap_fc = json.loads(overlap.to_json())

    # rasterize reclassified pov inc and overlap results
    rasterized_povinc, pi_profile = convert_to_raster(
        feature_collection=reclassed_pi_fc, resolution=30,
        crs=crs
    )
    rasterized_bounds, bnds_profile = convert_to_raster(
        feature_collection=overlap_fc, resolution=30,
        crs=crs
    )

    logger.debug(bnds_profile)
    # TODO: align rasterized bounds


    # run logical combination of rasterized overlap results and pov inc
    # log_com = logical_combination(array_1=rasterized_povinc,array_2=rasterized_bounds)
# 
    # with rio.open(
        # fp='./tests/data/flood-impact.tiff',mode='w', **bnds_profile
    # ) as src:
        # src.write(log_com,1)
# 
    return