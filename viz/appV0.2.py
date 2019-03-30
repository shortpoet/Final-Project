from flask import Flask, render_template, redirect, url_for, jsonify, request
from flaskext.mysql import MySQL
import json
import re
from datetime import datetime as dt

app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'cocktailproject'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    return render_template("index.html")

@app.route("/cocktails", methods=['GET', 'POST'])
def cocktails():

    if request.method == 'GET':

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Categories")
        category_table = cursor.fetchall()
        cursor.close()

        categories = []
        for i in category_table:
            this_cat = {}
            this_cat['Category_ID_Categories'] = i[0]
            this_cat['Category_Name'] = i[1]
            categories.append(this_cat)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cocktails")
        cocktail_table = cursor.fetchall()
        cursor.close()

        cocktails = []
        for i in cocktail_table:
            this_cock = {}
            this_cock['Cocktail_ID_Cocktails'] = i[0]
            this_cock['Cocktail_Name'] = i[1]
            this_cock['Glass_ID_Cocktails'] = i[2]
            this_cock['Category_ID_Cocktails'] = i[3]
            this_cock['Instruction'] = i[4]
            cocktails.append(this_cock)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Garnish_Instructions")
        garnish_instructions_table = cursor.fetchall()
        cursor.close()

        garnish_instructions = []
        for i in garnish_instructions_table:
            this_gi = {}
            this_gi['Garnish_Instruction_ID'] = i[0]
            this_gi['Cocktail_ID_Garnish_Instruction'] = i[1]
            this_gi['Garnish_ID_Garnish_Instructions'] = i[2]
            garnish_instructions.append(this_gi)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Garnishes")
        garnishes_table = cursor.fetchall()
        cursor.close()

        garnishes = []
        for i in garnishes_table:
            this_g = {}
            this_g['Garnish_ID_Garnishes'] = i[0]
            this_g['Garnish_Name'] = i[1]
            garnishes.append(this_g)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM glasses")
        glasses_table = cursor.fetchall()
        cursor.close()

        glasses = []
        for i in glasses_table:
            this_gl = {}
            this_gl['Glass_ID_Glasses'] = i[0]
            this_gl['Glass_Name'] = i[1]
            this_gl['Glass_Size'] = i[2]
            this_gl['Mask'] = i[3][1:]
            this_gl['Path'] = i[4][1:]
            this_gl['Mask_Height'] = i[5]
            this_gl['Mask_Top_Margin'] = i[6]
            glasses.append(this_gl)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Liquid_Instructions")
        liquid_instructions_table = cursor.fetchall()
        cursor.close()

        liquid_instructions = []
        for i in liquid_instructions_table:
            this_liq_ins = {}
            this_liq_ins['Liquid_Instructions'] = i[0]
            this_liq_ins['Cocktail_ID_Liquid_Instructions'] = i[1]
            this_liq_ins['Liquid_ID_Liquid_Instructions'] = i[2]
            this_liq_ins['Measure'] = i[3]
            this_liq_ins['Measure_Float'] = i[4]
            liquid_instructions.append(this_liq_ins)
            
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Liquids")
        liquids_table = cursor.fetchall()
        cursor.close()

        liquids = []
        for i in liquids_table:
            this_liq = {}
            this_liq['Liquid_ID_Liquids'] = i[0]
            this_liq['Liquid_Name'] = i[1]
            this_liq['Color'] = i[2]
            liquids.append(this_liq)

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Ratings")
        ratings_table = cursor.fetchall()
        cursor.close()

        ratings = []
        for i in ratings_table:
            this_rat = {}
            this_rat['Rating_ID'] = i[0]
            this_rat['Rating'] = i[1]
            this_rat['Cocktail_ID_Ratings'] = i[2]
            ratings.append(this_rat)

        for cat in categories:
            for cock in cocktails:
                if cat['Category_ID_Categories'] == cock['Category_ID_Cocktails']:
                    cock['Category_Name'] = cat['Category_Name']
        
        for g in garnishes:
            for gi in garnish_instructions:
                if g['Garnish_ID_Garnishes'] == gi['Garnish_ID_Garnish_Instructions']:
                    gi['Garnish_Name'] = g['Garnish_Name']

        for gi in garnish_instructions:
            for cock in cocktails:
                if gi['Cocktail_ID_Garnish_Instruction'] == cock['Cocktail_ID_Cocktails']:
                    cock['Garnish_Instruction_ID'] = gi['Garnish_Instruction_ID']
                    cock['Garnish_ID_Garnish_Instructions'] = gi['Garnish_ID_Garnish_Instructions']

        for glass in glasses:
            for cock in cocktails:
                cock['Ingredients'] = []
                cock['Ratings'] = []
                if glass['Glass_ID_Glasses'] == cock['Glass_ID_Cocktails']:
                    cock['Glass_Name']  = glass['Glass_Name'] 
                    cock['Glass_Size'] = glass['Glass_Size']
                    cock['Mask'] = glass['Mask']
                    cock['Path'] = glass['Path']
                    cock['Mask_Height'] = glass['Mask_Height']
                    cock['Mask_Top_Margin']  = glass['Mask_Top_Margin'] 

        for liq in liquids:
            for liq_ins in liquid_instructions:
                if liq['Liquid_ID_Liquids'] == liq_ins['Liquid_ID_Liquid_Instructions']:
                    liq_ins['Liquid_Name'] = liq['Liquid_Name']
                    liq_ins['Color'] = liq['Color']

        for liq_ins in liquid_instructions:
            for cock in cocktails:
                if liq_ins['Cocktail_ID_Liquid_Instructions'] == cock['Cocktail_ID_Cocktails']:
                    this_ing = {}
                    this_ing['Liquid_Instructions'] = liq_ins['Liquid_Instructions']
                    this_ing['Liquid_ID_Liquid_Instructions'] = liq_ins['Liquid_ID_Liquid_Instructions']
                    this_ing['Measure'] = liq_ins['Measure']
                    this_ing['Measure_Float'] = liq_ins['Measure_Float']
                    this_ing['Liquid_Name'] = liq_ins['Liquid_Name']
                    this_ing['Color'] = liq_ins['Color']
                    cock['Ingredients'].append(this_ing)

        for rat in ratings:
            for cock in cocktails:
                if rat['Cocktail_ID_Ratings'] == cock['Cocktail_ID_Cocktails']:
                    this_rat = {}
                    this_rat['Rating_ID'] = rat['Rating_ID']
                    this_rat['Rating'] = rat['Rating']
                    cock['Ratings'].append(this_rat)
            
        
        for cocktail in cocktails:
            measures = []
            for ingredient in cocktail['Ingredients']:
                for k, v in ingredient.items():
                    if k == 'Measure_Float':
                        measures.append(int(v))
                total = sum(measures)
                cocktail['Total_Volume'] = total
        
        for cocktail in cocktails:
            ratings = []
            for rating in cocktail['Ratings']:
                for k, v in rating.items():
                    if k == 'Rating':
                        ratings.append(int(v))
            average = round(sum(ratings)/len(ratings))
            cocktail['Average_Rating'] = average

        return jsonify(cocktails)

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
        # mongo.db.recipe_dump.update_one({'name': recipe}, {"$set": {'rating': this_rating}}, upsert=True)
        return redirect(url_for("glasses"))

@app.route("/liquids")
def liquids():

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Liquids")
    liquids_table = cursor.fetchall()
    liquids = []
    for i in liquids_table:
        this_liq = {}
        this_liq['Liquid_ID_Liquids'] = i[0]
        this_liq['Liquid_Name'] = i[1]
        this_liq['Color'] = i[2]
        liquids.append(this_liq)
    return jsonify(liquids)

@app.route("/table")
def table():
    return render_template("table.html")

@app.route("/glasses")
def glasses():
    return render_template("glasses.html")




# @app.route("/status_spirit.html#recient")
# def redir1():
#     return redirect(url_for("https://mars.nasa.gov/mer/mission/status_spirit.html#recient"))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000', debug=True)

