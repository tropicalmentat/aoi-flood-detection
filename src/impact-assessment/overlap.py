# for overlap analysis of extracted flood
# with municipal boundaries
import json
import geopandas as gpd
import logging
import osgeo.ogr as ogr
import osgeo.gdal as gdal

from shapely.geometry import shape
from shapely import (
    area, box, to_wkb
)

gdal.UseExceptions()

logger = logging.getLogger(__name__)
logging.getLogger('fiona').setLevel(logging.CRITICAL)

RECLASS_KEY = 'reclassified'

def get_filtered_data(in_ds, bbox):

    # Create Layer in flood_ds for clip geom
    in_layer = in_ds.GetLayer(0)

    logger.debug(in_layer.GetFeatureCount())
    in_layer.SetSpatialFilterRect(bbox[0],bbox[2],bbox[1],bbox[3])
    logger.debug(in_layer.GetFeatureCount())

    # initialize feature collection
    fc = {
        'type':'FeatureCollection',
        'features':[]
    }

    # we use getnextfeature to select filtered
    # features. getfeature only works with
    # indexes and we don't have any way of getting
    # filtered features directly by index
    for i in range(in_layer.GetFeatureCount()):
        feat = in_layer.GetNextFeature()
        if feat is not None:
            fc['features'].append(feat.ExportToJson(as_object=True))
        
    return fc

def initialize_data(flood_fpath, admin_bnds_fpath, pov_inc_fpath):

    pov_inc_ds = ogr.Open(pov_inc_fpath)
    admin_bnds_ds = ogr.Open(admin_bnds_fpath)
    flood_ds = ogr.Open(flood_fpath)

    flood_layer = flood_ds.GetLayer(0)
    # format: minx, maxx, miny, maxy
    flood_bbox = flood_layer.GetExtent()
    # flood_crs = flood_layer.GetSpatialRef().ExportToPROJJSON()

    in_layer = admin_bnds_ds.GetLayer(0)
    crs = in_layer.GetSpatialRef().ExportToPROJJSON()
    logger.debug(crs)

    logger.debug(in_layer.GetFeatureCount())
    in_layer.SetSpatialFilterRect(flood_bbox[0],flood_bbox[2],flood_bbox[1],flood_bbox[3])
    logger.debug(in_layer.GetFeatureCount())

    filtered_bounds = get_filtered_data(
        in_ds=admin_bnds_ds,bbox=flood_bbox
    )

    filtered_povinc = get_filtered_data(
        in_ds=pov_inc_ds,bbox=flood_bbox
    )

    flood_fc = {
        'type':'FeatureCollection',
        'features':[]
    }

    for i in range(flood_layer.GetFeatureCount()):
        feature = flood_layer.GetFeature(i)
        flood_fc['features'].append(
            feature.ExportToJson(as_object=True)
        )

    povinc_df = gpd.GeoDataFrame.from_features(filtered_povinc)
    bounds_df = gpd.GeoDataFrame.from_features(filtered_bounds)
    floods_df = gpd.GeoDataFrame.from_features(flood_fc)

    logger.debug(povinc_df.head())
    logger.debug(bounds_df.head())

    return bounds_df, povinc_df, floods_df, crs

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