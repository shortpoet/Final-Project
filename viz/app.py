from flask import Flask, render_template, redirect, Markup, url_for, jsonify
from flask_pymongo import PyMongo
import json
import re
from datetime import datetime as dt

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/cocktail_db"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/cocktail_db")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    return render_template("index.html")

@app.route("/cocktails")
def cocktails():

    cocktail_db_response = mongo.db.recipe_dump.find({}, {'_id': False})
    recipes = []
    for recipe in cocktail_db_response:
        recipes.append(recipe)
    # print(recipes)
    return jsonify(recipes)

@app.route("/table")
def table():
    return render_template("table.html")


# @app.route("/status_spirit.html#recient")
# def redir1():
#     return redirect(url_for("https://mars.nasa.gov/mer/mission/status_spirit.html#recient"))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=True)

