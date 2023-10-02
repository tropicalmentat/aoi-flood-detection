# Area-of-Interest Workflows for Manila Observatory's 

Containerized data processing workflows for Synthetic Aperture Radar (SAR) and optical imagery. The following sensors and platforms are supported:

1. Landsat 8 (Optical)
2. Sentinel2 (Optical)
2. ALOS2-PALSAR2 (SAR)
3. Sentinel1b (SAR)

# TODO: Add description of modules/files to use to generate flood extracts/data
### Repository Structure
- Each sensor (with the exception of Landsat8 and Sentinel2) have their own exclusive module in the `src` directory. This is because the raw data per sensor have different processing requirements, 
- The execution of the flood extraction workflow is facilitated by the `extract.py` script in each module. This script consolidates the pre-processing steps required for the raw data to be transformed to flood data. 
- The functions commonly used across the sensors are located in the `shared` directory.

### Requirements
- Git (to clone the repository)
- Docker 

### Usage


### Notes
- Sentinel 1 imagery

### References
- [Sentinel 1 RADAR](https://pro.arcgis.com/en/pro-app/latest/help/analysis/image-analyst/analysis-ready-sentinel-1-grd-data-generation.htm)
- [Sentinel 1 snappy example](https://github.com/wajuqi/Sentinel-1-preprocessing-using-Snappy/tree/master)
- [Sentinel 1 preprocessing](https://fivequestionz.home.blog/2020/01/31/how-to-preprocess-sentinel1-c-band-sar-image/)
- [pyradar](https://pyradar-tools.readthedocs.io/en/latest/tutorial.html)
- [Sentinel 2 Product Information](https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-2-msi/level-1c/algorithm-overview)
- [Landsat 8 Data User's Handbook](https://www.usgs.gov/landsat-missions/landsat-8-data-users-handbook)
- [ALOS2-PALSAR2 Info Sheets](https://www.eorc.jaxa.jp/ALOS/en/alos-2/datause/a2_format_e.htm)
