from flask import Flask, render_template, redirect, Markup, url_for, jsonify, request
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

@app.route("/cocktails", methods=['GET', 'POST'])
def cocktails():

    if request.method == 'GET':
        cocktail_db_response = mongo.db.recipe_db.find({}, {'_id': False})
        recipes = []
        for recipe in cocktail_db_response:
            # print(recipe)
            ratings = []
            print(recipe['rating'])
            for k, v in recipe['rating'].items():
                if k == 'rating':
                    ratings.append(int(v))
            average = round(sum(ratings)/len(ratings))
            recipe['avg_rating'] = average
            recipes.append(recipe)
        # print(recipes)
        return jsonify(recipes)

    if request.method == 'POST':
        form = request.form
        rating = request.form.get('submitRating')
        recipe = request.form.get('submitRecipe')
        print("====================")
        print(f"REQUEST: {request}")
        print(f"FORM: {form}")
        print(f"RATING: {rating}")
        print(f"RECIPE: {recipe}")
        print(f"DATE: {dt.now()}")
        print("====================")
        this_rating = {}
        this_rating['date_time'] = dt.now()
        this_rating['rating'] = rating
        mongo.db.recipe_dump.update_one({'name': recipe}, {"$set": {'rating': this_rating}}, upsert=True)
        return redirect(url_for("glasses"))

@app.route("/liquid")
def svgs():

    liquids_db_response = mongo.db.liquid_colors.find({}, {'_id': False})
    liquids = []
    for liquid in liquids_db_response:
        liquids.append(liquid)
    # print(recipes)
    return jsonify(liquids)

@app.route("/table")
def table():
    return render_template("table.html")

@app.route("/glasses")
def glasses():
    return render_template("glasses_old.html")




# @app.route("/status_spirit.html#recient")
# def redir1():
#     return redirect(url_for("https://mars.nasa.gov/mer/mission/status_spirit.html#recient"))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='8000', debug=True)

