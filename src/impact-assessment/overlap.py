# for overlap analysis of extracted flood
# with municipal boundaries
import json
import geopandas as gpd
import logging

from shapely.geometry import shape
from shapely import area

logger = logging.getLogger(__name__)
logging.getLogger('fiona').setLevel(logging.CRITICAL)

def initialize_data(flood_fpath, bounds_fpath):

    flood_df = None
    flood_crs = None
    bounds_df = None
    with open(flood_fpath,mode='r') as flood_src:
        flood_fc = json.loads(flood_src.read())
        flood_crs = flood_fc['crs']
        flood_df = gpd.GeoDataFrame.from_features(flood_fc)
    
    bounds_df = gpd.GeoDataFrame.from_file(bounds_fpath)
    
    flood_df.set_crs(flood_crs,inplace=True)

    logger.debug(bounds_df.crs)
    logger.debug(flood_df.crs)

    return flood_df, bounds_df

def overlap_analysis(
        flood: gpd.GeoDataFrame, bounds: gpd.GeoDataFrame
):
    
    flood.sindex
    count = 0
    for feature in bounds.iterfeatures():
        polygon = shape(feature['geometry'])
        bound_area = area(polygon)
        clipped = flood.clip(mask=polygon)
        flood_area = clipped.area.sum()
        if len(clipped) > 0:
            count += 1
            logger.debug(f'{flood_area} / {bound_area} = {flood_area*100/bound_area}')
        
    logger.debug(count)

    return