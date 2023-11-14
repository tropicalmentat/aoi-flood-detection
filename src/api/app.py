from flask import Flask

app = Flask(__name__)

img_fpath = './tests/data/rasterized.tiff'
img_bin = None

with open(file=img_fpath, mode='rb') as src:
    img_bin = src.read()

@app.route("/impact")
def get_flood_impact():

    # return "<p>Hello World!</p>"
    return img_bin