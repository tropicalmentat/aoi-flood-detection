import os
import xarray as xr
import numpy as np
import logging
import elevation
import osgeo.ogr as ogr
import xml.etree.ElementTree as ET
import rasterio as rio
import affine

from rasterio.profiles import DefaultGTiffProfile
from sarsen import (
    scene, 
    Sentinel1SarProduct,
    terrain_correction
)
from tempfile import NamedTemporaryFile
from rasterio import shutil as rio_shutil
from rasterio.vrt import WarpedVRT
from shapely.geometry import (
    GeometryCollection,
    box, 
    shape, 
)
from shapely import (
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

    return measurement, calibration, orbit_ecef, position_ecef

def init_datasets(
        safe_fp,bounds_fp,dem_fp,memmap_fn):

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
    left,bottom,right,top = total_bounds(intersect_box).tolist()

    logger.debug([left,bottom,right,top])
    # TODO convert coordinates back to wgs
    wgs_transformer = Transformer.from_crs(bounds_crs.to_epsg(),4326,always_xy=True)
    wgs_minx,wgs_miny = wgs_transformer.transform(left,bottom)
    wgs_maxx,wgs_maxy = wgs_transformer.transform(right,top)

    logger.debug([wgs_minx,wgs_miny,wgs_maxx,wgs_maxy])

    target_res = 90 # 90x90m
    utm_w = right - left
    utm_h = top - bottom
    pix_w = utm_w/target_res
    pix_h = utm_h/target_res
    target_transform = affine.Affine(
        target_res,0.0,left,
        0.0,-target_res,top
    )

    vrt_params = {
        'src_crs':src_crs, # force CGIAR DEM CRS
        'crs':bounds_crs,
        'transform':target_transform,
        'height':pix_h,
        'width':pix_w
    }

    # Open DEM file with UTM CRS using a warped vrt
    with NamedTemporaryFile() as tmp_dem,\
         rio.open(fp=dem_fp) as dem_src,\
         WarpedVRT(src_dataset=dem_src,**vrt_params) as dem_vrt:
        logger.debug(dem_src.profile)
        logger.debug(dem_vrt.profile)

        rio_shutil.copy(dem_vrt,tmp_dem.name,driver='GTiff')
         
        tmp_dem.seek(0)

        dem_kwargs = {"chunks":128}
        dem_raster = scene.open_dem_raster(tmp_dem.name,**dem_kwargs)
        convert_kwargs = {"source_crs":dem_vrt.profile.get('crs')}
        dem_ecef = scene.convert_to_dem_ecef(dem_raster,**convert_kwargs)
        logger.debug(dem_ecef)
        
        product = Sentinel1SarProduct(
            safe_fp,
            measurement_group="IW/VV"
        )
        logger.debug(product)

        # params borrowed from sarsen.apps.terrain_correction
        gtc_profile = DefaultGTiffProfile(
            transform=dem_vrt.profile.get('transform'),
            height=dem_vrt.profile.get('height'),
            width=dem_vrt.profile.get('width'),
            count=1,
            dtype=np.float32,
            compress='ZSTD',
            crs=bounds_crs,
            nodata=-99.0
        )

        gtc_mmp = np.memmap(
            filename=memmap_fn,
            dtype=gtc_profile.get('dtype'),
            shape=(gtc_profile.get('height'),gtc_profile.get('width'))
        )

        gtc = terrain_correction(
            product,
            dem_urlpath=tmp_dem.name,
            # correct_radiometry='gamma_bilinear',
            # radiometry_chunks=512,
            # grouping_area_factor=(1.0,2.0),
            # output_urlpath=f'./tests/data/gtc.tiff'
        )
        gtc_mmp[:] = gtc[:]

        gtc_mmp.flush()
        gtc = None

    return gtc_mmp, gtc_profile