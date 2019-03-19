from flask import Flask, render_template, redirect, Markup, url_for, jsonify
from flask_pymongo import PyMongo
from bson import json_util
import json
import re
from datetime import datetime as dt

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/asmr_youtube"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/social_blade")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    return render_template("index.html")

@app.route("/cocktails")
def asmr_channels():

    cocktail_db_response = mongo.db.cocktail.find_one({}, {'_id': False})
    asmr_data = []
    for channel, data in sb_db_response.items():
        asmr_data.append(data)
    for datum in asmr_data:


    return jsonify(asmr_data)

@app.route("/table")
def table():
    return render_template("table.html")


# @app.route("/status_spirit.html#recient")
# def redir1():
#     return redirect(url_for("https://mars.nasa.gov/mer/mission/status_spirit.html#recient"))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=True)

