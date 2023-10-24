# for overlap analysis of extracted flood
# with municipal boundaries
import json
import geopandas as gpd
import logging

from shapely.geometry import shape
from shapely import area

logger = logging.getLogger(__name__)
logging.getLogger('fiona').setLevel(logging.CRITICAL)

RECLASS_KEY = 'reclass'

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
    
    def reclassify(flooded):

        if flooded > 80:
            return 5
        elif flooded > 60 and flooded <= 80:
            return 4
        elif flooded > 40 and flooded <= 60:
            return 3
        elif flooded > 20 and flooded <= 40:
            return 2
        elif flooded <= 20:
            return 1

    flood.sindex
    geoprocessed = {
        'type' : 'FeatureCollection',
        'features' : []
    }
    for feature in bounds.iterfeatures():
        polygon = shape(feature['geometry'])
        bound_area = area(polygon)
        clipped = flood.clip(mask=polygon)
        flood_area = clipped.area.sum()
        if len(clipped) > 0:
            # logger.debug(f'{flood_area} / {bound_area} = {flood_area*100/bound_area}')
            feature['properties']['perc_flooded'] = flood_area*100/bound_area
            feature['properties'][RECLASS_KEY] = reclassify(
                feature['properties']['perc_flooded'])
            geoprocessed['features'].append(feature)
    
    analyzed = gpd.GeoDataFrame.from_features(geoprocessed, crs=bounds.crs)

    return analyzed

def poverty_incidence_reclassify(pov_data):

    def reclassify(pov_inc):

        if pov_inc > 80:
            return 5
        elif pov_inc > 60 and pov_inc <= 80:
            return 4
        elif pov_inc > 40 and pov_inc <= 60:
            return 3
        elif pov_inc > 20 and pov_inc <= 40:
            return 2
        elif pov_inc <= 20:
            return 1

    pov_inc = pov_data.Poverty_In

    pov_data[RECLASS_KEY] = pov_inc.apply(lambda x: reclassify(x))

    return pov_data