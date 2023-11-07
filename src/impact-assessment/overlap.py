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

logger = logging.getLogger(__name__)
logging.getLogger('fiona').setLevel(logging.CRITICAL)

RECLASS_KEY = 'reclassified'

def initialize_data(flood_fpath, admin_bnds_fpath, pov_inc_fpath):

    mem_driver = ogr.GetDriverByName('MEMORY')

    pov_inc_ds = ogr.Open(pov_inc_fpath)
    admin_bnds_ds = ogr.Open(admin_bnds_fpath)
    flood_ds = ogr.Open(flood_fpath)
    clip_ds = mem_driver.CreateDataSource('clip_ds')
    out_ds = mem_driver.CreateDataSource('out_ds')

    mem_driver.Open('clip_ds',1)
    mem_driver.Open('out_ds',1)

    # format: minx, maxx, miny, maxy
    flood_bbox = flood_ds.GetLayer(0).GetExtent()

    flood_crs = flood_ds.GetLayer(0).GetSpatialRef()

    logger.debug(flood_bbox)
    bbox_geom = ogr.CreateGeometryFromWkb(to_wkb(box(
        xmin=flood_bbox[0], ymin=flood_bbox[2], xmax=flood_bbox[1], ymax=flood_bbox[3]
        ), include_srid=True))

    logger.debug(bbox_geom)

    # Create Layer in flood_ds for clip geom
    out_layer = out_ds.CreateLayer('out')
    clip_layer = clip_ds.CreateLayer('clip')
    geom_field_defn = ogr.GeomFieldDefn()
    geom_field_defn.SetName('geom')
    geom_field_defn.SetType(bbox_geom.GetGeometryType())
    geom_field_defn.SetSpatialRef(flood_crs)

    clip_layer.CreateGeomField(geom_field_defn)

    clip_feat_defn = ogr.FeatureDefn()
    clip_feat_defn.AddGeomFieldDefn(geom_field_defn)

    clip_feature = ogr.Feature(clip_feat_defn)
    clip_feature.SetGeometry(bbox_geom)

    clip_layer.CreateFeature(clip_feature)

    result = admin_bnds_ds.GetLayer(0).Clip(method_layer=clip_layer,result_layer=out_layer)

    logger.debug(out_layer.GetFeatureCount())
    # this is slow for large files
    # because of serialized reading of
    # shp files using fiona lib
    # flood_df = None
    # flood_crs = None
    # bounds_df = None
    # with open(flood_fpath,mode='r') as flood_src:
    #     flood_fc = json.loads(flood_src.read())
    #     flood_crs = flood_fc['crs']
    #     flood_df = gpd.GeoDataFrame.from_features(flood_fc)
    
    # bounds_df = gpd.GeoDataFrame.from_file(admin_bnds_fpath)
    # bounds_bbox = bounds_df.total_bounds
    
    # flood_df.set_crs(flood_crs,inplace=True)

    # logger.debug(bounds_df.crs)
    # logger.debug(flood_df.crs)

    # return flood_df, bounds_df

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