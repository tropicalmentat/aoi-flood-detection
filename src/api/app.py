from flask import Flask

app = Flask(__name__)

@app.route("/")
def get_flood_impact():

    return "<p>Hello World!</p>"