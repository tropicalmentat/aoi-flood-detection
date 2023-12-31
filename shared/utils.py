from tempfile import NamedTemporaryFile
from rasterio.warp import calculate_default_transform, reproject, aligned_target
from rasterio.windows import Window
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from rasterio.profiles import DefaultGTiffProfile
from pyproj import Transformer
from shapely import get_coordinates, set_coordinates
from shapely.geometry import shape, mapping, GeometryCollection
from xrspatial.local import combine
from xarray import merge, DataArray

import rasterio as rio
import numpy as np
import numpy.ma as ma
import logging

logger = logging.getLogger(__name__)
logging.getLogger('rasterio').setLevel(logging.CRITICAL)

RECLASS_KEY = 'reclassified'

def get_nodata_mask(array: np.ndarray, profile: dict):

    mask = np.where(array==profile['nodata'],True,False)

    return mask

def load_image(fpath):
    img = None
    with open(file=fpath,mode='rb') as tif:
        img = tif.read()
    return img

def image_to_array(
        img: bytes, masked: bool = True, band_idx: int=1,
        cols: tuple=None, rows:tuple=None):
    with NamedTemporaryFile(mode='wb',suffix='.tif') as tmp:
        tmp.write(img)
        tmp.seek(0)
        with NamedTemporaryFile() as tmp_array:
            with rio.open(fp=tmp.name) as src:
                profile = src.profile
                logger.debug(profile)
                bounds = src.bounds
                if cols is not None and rows is not None:
                    window = Window.from_slices(rows=rows,cols=cols)
                    win_bounds = src.window_bounds(window)
                    win_transform = src.window_transform(window)
                    profile['transform'] = win_transform
                    profile['width'] = cols[1]
                    profile['height'] = rows[1]
                    logger.debug(profile)
                    array = np.memmap(
                        filename=tmp_array.name,dtype=profile['dtype'],mode='w+',
                        shape = (rows[1],cols[1])
                    )
                    src.read(band_idx,out=array,window=window)
                    logger.debug(array)
                    logger.debug(array.shape)

                    return array, profile, win_bounds
                else:
                    array = np.memmap(
                        filename=tmp_array.name,dtype=profile['dtype'],mode='w+',
                        shape = src.shape
                    )
                    logger.debug(band_idx)
                    logger.debug(array)
                    src.read(band_idx,out=array)
                    logger.debug(array.shape)

                    return array, profile, bounds

def build_landsat_metadata(landsat_mtl_fp):

    metadata = {}
    with open(landsat_mtl_fp) as mtl:
        for ln in mtl.readlines():
            if 'GROUP' in ln: # skip group headers
                continue
            key = ln.split('=')[0].strip(' ')
            # handle the numerical values as float
            # and the string values as text
            try:
                value = float(ln.split('=')[1].strip(' ').strip('\n'))
            except Exception as e:
                # logger.warning(e)
                try:
                    value = ln.split('=')[1].strip(' ').strip('\n') 
                except Exception as e:
                    # logger.error(e)
                    continue
            metadata[key] = value

    return metadata

def build_alos2palsar2_metadata(metadata_fp):
    # collect geocode information
    metadata = {}
    with open(file=metadata_fp,mode='r') as summary:
        for ln in summary.readlines():
            key = ln.split('=')[0]
            try:
                value = float(ln.split('=')[1].replace('"','').strip('\n'))
            except Exception as e:
                try:
                    value = ln.split('=')[1].replace('"','').strip('\n')
                except Exception as e:
                    continue
            metadata[key] = value
    logger.debug(metadata)
    return metadata

def derive_minmax_coords(profile):
    # determine the min and max longitude/easting 
    # and latitude/northing
    width = profile['width']
    height = profile['height']
    gdal_format = profile['transform'].to_gdal()
    logger.debug(gdal_format)
    minx=gdal_format[0]
    maxx=gdal_format[0] + gdal_format[1]*width + gdal_format[1]
    miny=gdal_format[3]
    maxy=gdal_format[3] + gdal_format[5]*height + gdal_format[5]
    logger.debug(f'({minx},{miny},{maxx},{maxy}')
    return (minx,miny,maxx,maxy)

def get_earth_sun_distance(data: str):

    distance = None

    for ln in data.readlines():
        if 'EARTH_SUN_DISTANCE' in ln:
            distance = float(ln.split('=')[1].strip(' '))
            logger.debug(type(distance))
            logger.debug(distance)
    return distance

def project_image(band: np.ndarray, src_bounds, src_profile, src_crs, dst_crs):
    logger.debug(src_bounds.top)
    transform,w,h = calculate_default_transform(src_crs=src_crs,
                                                dst_crs=dst_crs,
                                                width=src_profile['width'],
                                                height=src_profile['height'],
                                                left=src_bounds.left,
                                                bottom=src_bounds.bottom,
                                                right=src_bounds.right,
                                                top=src_bounds.top)
    logger.debug((h,w))
    with NamedTemporaryFile() as tmp:
        output = np.memmap(
            filename=tmp.name,dtype=band.dtype,shape=(h,w))
        logger.debug(src_profile['transform'].to_gdal())
        logger.debug(transform.to_gdal())
        logger.debug(band.shape)
        logger.debug(output.shape)
    
        reproject(source=band,
                  destination=output,
                  src_crs=src_crs,
                  dst_crs=dst_crs,
                  src_transform=src_profile['transform'],
                  dst_transform=transform)
        
        return output

def project_coordinates(feature_collection,src_crs,dst_crs):
    transformer = Transformer.from_crs(src_crs,dst_crs,always_xy=True)
    projected_fc = {
        'type':'FeatureCollection',
        'features':[],
        'crs':dst_crs.to_string()
    }
    for feature in feature_collection['features']:
        geometry = shape(feature['geometry'])
        projected_coords = []
        for coords in get_coordinates(geometry):
            projected_coords.append(list(transformer.transform(coords[0],coords[1])))
        set_coordinates(geometry,projected_coords)
        projected_feature = {
            'type':'Feature',
            'geometry':mapping(geometry),
            'properties':{
                'value':1.0
            }
        }
        projected_fc['features'].append(projected_feature)
    return projected_fc

def convert_to_raster(
        feature_collection, crs, resolution,
        ):
    iter_pairs = [
        (feat['geometry'],feat['properties'][RECLASS_KEY]) for feat in feature_collection['features']
    ]
    
    mp = GeometryCollection(geoms=[
        shape(feat['geometry']) for feat in feature_collection['features']
    ])
    
    # shapely bounds returns coords in 
    # the following tuple: 
    # (xmin, ymin, xmax, ymax)
    # will be used to as the raster bounds
    # which has the form 
    # (lower left x, lower left y, upper right x, upper right y)
    bounds = mp.bounds
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    
    # array shape in the form
    # (height, width)
    array_shape = (round(height), round(width))

    logger.debug(bounds)
    logger.debug(f'height:{height}, width:{width}')

    # we use the bounds information
    # of the geometry to define the
    # corresponding array
    src_transform = from_bounds(
        west=bounds[0], south=bounds[1], east=bounds[2], north=bounds[3], 
        width=width, height=height
        )
    logger.debug(src_transform)

    dst_transform,dst_w,dst_h = aligned_target(
    transform=src_transform, width=width, height=height, resolution=(resolution,resolution)
        )
    logger.debug(dst_transform)
    # TODO: nodata as func param
    profile = DefaultGTiffProfile(data={
        'width':dst_w, 'height':dst_h, 'crs':crs, 'transform':dst_transform,
        'nodata':0, 'dtype':np.int16, 'count':1
    })

    col_offsets = [i for i in range(0,profile['width'],profile['blockxsize'])]
    row_offsets = [i for i in range(0,profile['height'],profile['blockysize'])]

    offsets = []

    for col in col_offsets:
        for row in row_offsets:
            offsets.append((col,row))
    
    with NamedTemporaryFile() as tmp_rast:
        rasterized = np.memmap(
            filename=tmp_rast, dtype=np.int16,
            shape=array_shape
        )

        rasterize(
            shapes=iter_pairs, out_shape=(dst_h,dst_w),
            transform=dst_transform, out=rasterized, dtype='int16'
            )
    
        rasterized.flush()
        # TODO: Put filepath as func param
        with rio.open(
            fp=f'./tests/data/rasterized.tiff', mode='w', **profile
        ) as tif:
            for pair in offsets:
                if pair[0] == col_offsets[-1] or pair[1] == row_offsets[-1]:
                    window = Window.from_slices(
                        cols=(pair[0],profile['width']), rows=(pair[1],profile['height'])
                        )
                    slice = window.toslices()
                    logger.debug(slice)
                    tif.write(rasterized[slice],window=window,indexes=1)
                else:
                    window = Window(
                        col_off=pair[0],row_off=pair[1],
                        width=profile['blockxsize'], height=profile['blockysize']
                    )
                    slice = window.toslices()
                    logger.debug(slice)
                    tif.write(rasterized[slice],window=window,indexes=1)

    return rasterized, profile

def logical_combination(array_1, array_2):
    raster_ds = merge(
        [DataArray(data=array_1,name='flood'), DataArray(array_2,name='pov')],
        join='exact',compat='minimal')
    
    logger.debug(raster_ds)
 
    combined = combine(raster=raster_ds[['pov','flood']],data_vars=['pov','flood'])
# 
    return combined.to_numpy()