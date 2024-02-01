import os
import json
import xarray as xr
import logging
import elevation
import osgeo.ogr as ogr
import xml.etree.ElementTree as ET
from sarsen import apps
from shapely.geometry import (
    MultiPolygon,
    GeometryCollection,
    box, 
    shape, 
    mapping
)
from shapely import (
    get_coordinates,
    set_coordinates,
    bounds,
    intersection,
    total_bounds
)
from pyproj.crs import CRS
from pyproj import Transformer

logger = logging.getLogger(__name__)
logging.getLogger("xmlschema").setLevel(logging.CRITICAL)

def geocode_img(fp):
    calibration_group = "IW/VH/calibration"
    measurement_group = 'IW/VH'
    orbit_group = f'{measurement_group}/orbit'
    kwargs = {'chunks':2048}

    calibration = xr.open_dataset(
        fp,engine="sentinel-1",group=calibration_group,**kwargs)
    beta_nought_lut = calibration.betaNought
    logger.debug(calibration)
    logger.debug(beta_nought_lut)

    measurement_ds = xr.open_dataset(
        fp, engine='sentinel-1', group=measurement_group,**kwargs)
    measurement = measurement_ds.measurement
    
    orbit_ecef = xr.open_dataset(
        fp,engine='sentinel-1', group=orbit_group, **kwargs
    )
    position_ecef = orbit_ecef.position

    logger.debug(measurement)
    logger.debug(calibration)
    logger.debug(orbit_ecef)
    logger.debug(position_ecef)
    return

def init_datasets(safe_fp,bounds_fp):

    # CRS of raw sentinel1b image
    src_crs = CRS.from_epsg(4326)

    # Get manifest.safe file
    manifest_fp = os.path.join(safe_fp,'manifest.safe')

    tree = ET.parse(manifest_fp)
    root = tree.getroot()

    lats = None
    lons = None
    for child in root:
        if 'metadata' in child.tag:
            for gc in child:
                if 'measurementFrameSet' in gc.attrib.get('ID'):
                    for subelm in gc.iter():
                        if 'coordinates' in subelm.tag:
                            logger.debug(subelm.text)
                            raw = [pair.split(',') for pair in subelm.text.split(' ')]
                            lats = sorted([(float(pair[0])) for pair in raw])
                            lons = sorted([(float(pair[1])) for pair in raw])


    bounds_ds = ogr.Open(bounds_fp)
    bounds_layer = bounds_ds.GetLayer(0)
    bounds_crs = CRS.from_json(bounds_layer.GetSpatialRef().ExportToPROJJSON())
    logger.debug(bounds_crs.to_epsg())

    box_geom = box(
        lons[0],lats[0],lons[-1],lats[-1]
    )    
    bbox = total_bounds(box_geom).tolist()

    transformer = Transformer.from_crs(4326,bounds_crs.to_epsg(),always_xy=True)
    minx,miny = transformer.transform(bbox[0],bbox[1])
    maxx,maxy = transformer.transform(bbox[2],bbox[3])

    logger.debug(bounds_layer.GetFeatureCount())
    logger.debug(bounds_layer.GetExtent(1))
    bounds_layer.SetSpatialFilterRect(
        minx,miny,maxx,maxy
        )
    logger.debug(bounds_layer.GetFeatureCount())
    logger.debug(bounds_layer.GetExtent(1))

    polygons = []

    for feat in range(bounds_layer.GetFeatureCount()):
        feat = bounds_layer.GetNextFeature()
        if feat is not None:
            feature = feat.ExportToJson(as_object=True)
            polygons.append(shape(feature['geometry']))
    
    geom_clxn = GeometryCollection(polygons)

    geom_clxn_bounds = total_bounds(geom_clxn).tolist()

    utm_box = box(
        minx,miny,maxx,maxy
    )
    aoi_box = box(
        geom_clxn_bounds[0],geom_clxn_bounds[1],
        geom_clxn_bounds[2],geom_clxn_bounds[3]
    )

    intersect_box = intersection(aoi_box,utm_box)
    intersect_bounds = total_bounds(intersect_box)

    logger.debug(intersect_bounds)
    # fc = {
    #     'type':'FeatureCollection',
    #     'features':[
    #         {
    #             'type':'Feature',
    #             'geometry':mapping(intersect_box)
    #         }
    #     ]
    # }
    # with open(file=f'./tests/data/intersect_box.json',mode='w') as tmp:
    #     tmp.write(json.dumps(fc))
    
    elevation.clip(bounds=(
        intersect_bounds[0],intersect_bounds[1],
        intersect_bounds[2],intersect_bounds[3]
    ),
        product='SRTM3'.
        output=f'./tests/dem.tif'
    )
    return