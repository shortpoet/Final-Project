from credentials_local import user, password, rds_host
import pymysql
import pandas as pd
from boston_functions import *
from fractions import Fraction
import re
import numpy as np
from liquid import liquids
from garnish import garnishes
import random

#set options so data isn't TRUNCATED!! 
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)  

#import mr boston cocktail database
data = pd.read_csv("./mr-boston-all-glasses.csv")
#locate data
data = data[data.loc[:, "glass-size"].notna()]

valid_units = ["oz", "tsp", "splash", "dash"]

fill_liquid = ["ginger ale", "carbonated water", "cola", "water", "chilled champagne", "soda water", 
               "club soda", "ginger ale or soda water", "lemon-lime soda", "ginger beer", "bitter lemon soda",
               "apple juice", "orange juice"]

invaild_ingredients = ['chopped', 'cut in half', 'cut in halves', 'cut into halves', 'flamed', 'hulled', 'long',
                       'skinned','whipped', "preferably b.a. reynold's", 'preferably jamaican', 'preferably japanese', 
                       'preferably pedro ximenez', "such as bittermen's elemakule", 'such as demerara', 
                       'such as islay or skye', 'such as nasturtium']

ingredient_indicies = range(3, 14)

#get all recipe data
all_recipies, measures = get_cocktail_recipies(data, ingredient_indicies, liquids, garnishes, invaild_ingredients, valid_units)

#set categories list
categories = list(set(data.iloc[:, 1])) + ["AI Instant Classic"]

############################
# COCKTAIL RECIPES TO TEXT #
############################
with open('mr_boston_cocktails.txt', 'w') as text_file:
    for i in range(len(all_recipies)):
        cocktail_string = all_recipies[i]['name'] + " - "
        cocktail_string += all_recipies[i]['glass'] + " - "
        for measurement, ingredient in all_recipies[i]["recipe"]:
            cocktail_string += measurement + " " + ingredient + " - "
        cocktail_string += all_recipies[i]['instructions']
        text_file.write(cocktail_string + "\n")


###################
# POPULATE TABLES #
###################

####################
### LIQUID TABLE ###
####################
#import colors for liquids
liquid_colors = pd.read_csv("./Liquid_Colors_Final.csv")

def populate_liquid_table(liquid_df):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for row in range(len(liquid_df)):
        liquid = liquid_df.iloc[row, 0]
        hex_color = liquid_df.iloc[row, 1]
        print(liquid, hex_color)
        sql = f"INSERT INTO Liquids (Liquid_Name, Color) VALUES ('{liquid}', '{hex_color}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Liquids")
    data = cursor.fetchall()
    print("++++++++Liquid Table Populated+++++++++")
    conn.close()
populate_liquid_table(liquid_colors)

#####################
### GARNISH TABLE ###
#####################
def populate_garnish_table(garnishes):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for garnish in garnishes:
        print(garnish)
        sql = f"INSERT INTO Garnishes (Garnish_Name) VALUES ('{garnish}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Garnishes")
    data = cursor.fetchall()
    print("++++++Garnish Table Populated+++++++++")
    conn.close()
populate_garnish_table(garnishes)

######################
### CATEGORY TABLE ###
######################
def populate_category_table(categories):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for category in categories:
        print(category)
        sql = f"INSERT INTO Categories (Category_Name) VALUES ('{category}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Categories")
    data = cursor.fetchall()
    print("+++++++++Category Table Populated+++++++++")
    conn.close()
populate_category_table(categories)

###################
### GLASS TABLE ###
###################
#set empty lists for cocktail names, glass names, and glass sizes
names = []
glasses = []
glass_sizes = []

# locate cocktail names, glass names, and glass sizes
for i in range(len(all_recipies)):
    names.append(all_recipies[i]["name"])
    glasses.append(all_recipies[i]["glass"])
    glass_sizes.append(all_recipies[i]["glass_size"])
#create glass df
glass_df = pd.DataFrame({"cocktail_name": names, "glass_name": glasses, "glass_size": glass_sizes})

### GLASS SVG DATA ###
#import glass svg data
svg_data = pd.read_csv("../the_glasses.csv")

#set empty lists for svg data
masks = []
paths = []
mask_heights = []
mask_top_margins = []

#match mr. boston  db glass names with svg glass names
for i in range(len(glass_df)):
    glass_name = glass_df.iloc[i, 1]
    if glass_name == "Beer Mug":
        df = svg_data.loc[svg_data["name"]=="fluted_lager", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif (glass_name == "Brandy Snifter") or (glass_name == "Red-Wine Glass") or (glass_name == "White-Wine Glass"):
        df = svg_data.loc[svg_data["name"]=="poco_grande", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Champagne Flute":
        df = svg_data.loc[svg_data["name"]=="champagne_extra_fluted", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Cocktail Glass":
        df = svg_data.loc[svg_data["name"]=="cocktail_lg", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Collins Glass":
        df = svg_data.loc[svg_data["name"]=="collins", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif (glass_name == "Cordial or Pony Glass") or (glass_name == "Pousse-Cafe Glass") or (glass_name == "Sherry Glass"):
        df = svg_data.loc[svg_data["name"]=="pousse_cafe", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Highball Glass":
        df = svg_data.loc[svg_data["name"]=="highball", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Hurricane Glass":
        df = svg_data.loc[svg_data["name"]=="hurricane", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Irish Coffee Glass":
        df = svg_data.loc[svg_data["name"]=="irish_coffee", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Old-Fashioned Glass":
        df = svg_data.loc[svg_data["name"]=="old_fashioned", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif (glass_name == "Punch Cup") or (glass_name == "Shot Glass"):
        df = svg_data.loc[svg_data["name"]=="rocks", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))
    elif glass_name == "Sour Glass":
        df = svg_data.loc[svg_data["name"]=="champagne_flute", :]
        masks.append(df["mask"].to_string(index=False))
        paths.append(df["path"].to_string(index=False))
        mask_heights.append(df["maskHeight"].to_string(index=False))
        mask_top_margins.append(df["maskTopMargin"].to_string(index=False))

#add svg info to glass df
glass_df["mask"] = masks
glass_df["path"] = paths
glass_df["mask_height"] = mask_heights
glass_df["mask_top_margin"] = mask_top_margins
glass_df.head()

def populate_glass_table(glass_df):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for row in range(len(glass_df)):
        glass_name = glass_df.iloc[row, 1]
        glass_size = glass_df.iloc[row, 2]
        mask = glass_df.iloc[row, 3]
        path = glass_df.iloc[row, 4]
        mask_height = glass_df.iloc[row, 5]
        mask_top_margin = glass_df.iloc[row, 6]
        print(glass_name)
        sql = f"INSERT INTO Glasses (Glass_Name, Glass_Size, Mask, Path, Mask_Height, Mask_Top_Margin) VALUES ('{glass_name}', '{glass_size}', '{mask}', '{path}', '{mask_height}', '{mask_top_margin}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Glasses")
    data = cursor.fetchall()
    print("+++++++Glasses Table Populated++++++")
    conn.close()
populate_glass_table(glass_df)
    
    
######################
### COCKTAIL TABLE ###
######################
#set empty lists for instructions, category and glass ids
category_ids = []
glass_ids = []
instructions_list = []

#connect to sql
conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
#create cursor object
cursor = conn.cursor()
#use cocktail db
cursor.execute('USE cocktailproject')

#for each recipe,
for i in range(len(all_recipies)):
    #find instructions and append to instructions list
    instructions = all_recipies[i]["instructions"]
    instructions = re.sub(r'["]', '\'', instructions)
    instructions_list.append(instructions)
    
    #find cocktail category
    category = all_recipies[i]["category"]
    
    #select category id and append to category id list
    sql = f"SELECT Category_ID FROM Categories WHERE Category_Name='{category}'"
    cursor.execute(sql)
    data = cursor.fetchall()
    category_ids.append(data[0][0])
    
    #select glass id and append to glass id list
    sql = f"SELECT Glass_ID FROM Glasses WHERE Glass_Name='{glasses[i]}'"
    cursor.execute(sql)
    data = cursor.fetchall()
    glass_ids.append(data[0][0])

#close sql connection
conn.close()

#create cocktail df
cocktail_df = pd.DataFrame({"cocktail_name": names, "glass_id": glass_ids, "category_ids": category_ids, "instructions": instructions_list})

def populate_cocktail_table(cocktail_df):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for row in range(len(cocktail_df)):
        cocktail_name = cocktail_df.iloc[row, 0]
        glass_id = cocktail_df.iloc[row, 1]
        category_id = cocktail_df.iloc[row, 2]
        instructions = cocktail_df.iloc[row, 3]
        print(cocktail_name)
        sql = f'INSERT INTO Cocktails (Cocktail_Name, Glass_ID, Category_ID, Instructions) VALUES ("{cocktail_name}", "{glass_id}", "{category_id}", "{instructions}");'
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Cocktails")
    data = cursor.fetchall()
    print("++++++Cocktail Table Populated++++++")
    conn.close()
populate_cocktail_table(cocktail_df)


###########################
### LIQUID INSTRUCTIONS ###
###########################
#set empty lists for liquid and cocktail ids, liquid ingredients and measures
liquid_ids_list = []
cocktail_ids = []
liquid_ingredient_list = []
liquid_measure_list = []
liquid_measure_float_list = []
cocktail_ids_list = []

#connect to sql, create cursor object, and use cocktail db
conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
cursor = conn.cursor()
cursor.execute('USE cocktailproject')
#construct and execute sql select statement
sql = "SELECT Cocktail_ID FROM Cocktails"
cursor.execute(sql)
data = cursor.fetchall()
#get cocktail id data
cocktail_ids_data = data

#add cocktail ids to list
for i in range(len(cocktail_ids_data)):
    cocktail_ids.append(cocktail_ids_data[i][0])

#close connection
conn.close()

#for each recipe,
for i in range(len(all_recipies)):
    #set cocktail_id
    cocktail_id = cocktail_ids[i]
    #find ingredient list
    ingredient_list = all_recipies[i]["recipe"]
    #find total glass volume
    total_glass_volume = all_recipies[i]["glass_size"]
    #set total liquid measure to 0
    total_liquid_measure = 0
    
    #for each non-garnish ingredient,
    for measure, ingredient in ingredient_list:
        measure = measure.strip()
        if measure == "add":
            pass
        elif ingredient == "pimm's cup":#pimm's cup did not make it onto out liquids list
            pass
        
        else:
            #add to lists
            cocktail_ids_list.append(cocktail_id)
            liquid_measure_list.append(measure)
            liquid_ingredient_list.append(ingredient)
            
        ### CONVERTING MEASURES TO FLOAT ###
            #split measure on spaces
            split_measure = measure.split(" ")

            #if measure is compound fraction,
            if len(split_measure) > 2:
                #recombine compound fraction
                measure = split_measure[0]+" "+split_measure[1]
                #convert to float
                measure_float = float(sum(Fraction(s) for s in measure.split()))
                #add to float list
                liquid_measure_float_list.append(measure_float)
                #add measure to drink's total measure
                total_liquid_measure += measure_float
            #if measure is an integer,
            elif len(split_measure) > 1:
                #convert to float
                measure_float = float(sum(Fraction(s) for s in split_measure[0].split()))
                #if unit is smaller than oz, convert measure to oz
                if split_measure[1][:3] == "tsp":
                    measure_float = measure_float / 6
                elif split_measure[1][:4] == "dash":
                    measure_float = measure_float / 32
                elif split_measure[1][:6] == "splash":
                    measure_float = measure_float / 5
                #add to float list
                liquid_measure_float_list.append(measure_float)
                #add measure to drink's total measure
                total_liquid_measure += measure_float
            #if measure if fill,
            elif split_measure[0] == "fill":
                #calculate remaining volume
                remaining_volume = float(total_glass_volume) - float(total_liquid_measure)
                #set fill measure to half remaining volume
                measure_float = float(remaining_volume / 2)
                #add to float list
                liquid_measure_float_list.append(measure_float)
            else:
                measure_float = float(0)
                liquid_measure_float_list.append(measure_float)

#connect to sql
conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
#create cursor object
cursor = conn.cursor()
#use cocktail db
cursor.execute('USE cocktailproject')

#for each ingredient,
for ingredient in liquid_ingredient_list:
    if ingredient[:6] == "rose's":
        ingredient = ingredient[7:]
        #select liquid id and append to liquid id list
        sql = f'SELECT Liquid_ID FROM Liquids WHERE Liquid_Name="{ingredient}"'
        cursor.execute(sql)
        data = cursor.fetchall()
        liquid_ids_list.append(data[0][0])
    elif ingredient[:8] =="peychaud": 
        ingredient = "peychauds bitters"
        #select liquid id and append to liquid id list
        sql = f'SELECT Liquid_ID FROM Liquids WHERE Liquid_Name="{ingredient}"'
        cursor.execute(sql)
        data = cursor.fetchall()
        liquid_ids_list.append(data[0][0])
    else:
        #select liquid id and append to liquid id list
        sql = f'SELECT Liquid_ID FROM Liquids WHERE Liquid_Name="{ingredient}"'
        cursor.execute(sql)
        data = cursor.fetchall()
        liquid_ids_list.append(data[0][0])

#close sql connection
conn.close()

#create liquid ingredients df
liquid_ingredients_df = pd.DataFrame({"cocktail_id": cocktail_ids_list, "liquid_id": liquid_ids_list, "measure": liquid_measure_list, "measure_float": liquid_measure_float_list})

def populate_liquid_instructions_table(liquid_instructions_df):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for row in range(len(liquid_instructions_df)):
        cocktail_id = liquid_instructions_df.iloc[row, 0]
        liquid_id = liquid_instructions_df.iloc[row, 1]
        measure = liquid_instructions_df.iloc[row, 2]
        measure_float = liquid_instructions_df.iloc[row, 3]
        print(cocktail_id, liquid_id, measure)
        sql = f'INSERT INTO Liquid_Instructions (Cocktail_ID, Liquid_ID, Measure, Measure_Float) VALUES ("{cocktail_id}", "{liquid_id}", "{measure}", "{measure_float}");'
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Liquid_Instructions")
    data = cursor.fetchall()
    print("++++++Liquid Ingredients Table Populated+++++++++")
    conn.close()
populate_liquid_instructions_table(liquid_ingredients_df)

############################
### GARNISH INSTRUCTIONS ###
############################
#set empty lists for garnish and cocktail ids, liquid ingredients and measures
garnish_ids_list = []
cocktail_ids_list = []
garnish_ingredient_list = []

#for each recipe,
for i in range(len(all_recipies)):
    #set cocktail_id
    cocktail_id = cocktail_ids[i]
    #find ingredient list
    ingredient_list = all_recipies[i]["recipe"]
    #for each garnish ingredient,
    for measure, ingredient in ingredient_list:
        if measure != "add":
            pass
        else:
            #add cocktails id and garnish to lists
            cocktail_ids_list.append(cocktail_id)
            garnish_ingredient_list.append(ingredient)
            
#connect to sql
conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
#create cursor object
cursor = conn.cursor()
#use cocktail db
cursor.execute('USE cocktailproject')

#for each ingredient,
for ingredient in garnish_ingredient_list:
    sql = f'SELECT Garnish_ID FROM Garnishes WHERE Garnish_Name="{ingredient}"'
    cursor.execute(sql)
    data = cursor.fetchall()
    #append garnish id
    garnish_ids_list.append(data[0][0])
    
#close sql connection
conn.close()

#create garnish ingredients df
garnish_ingredients_df = pd.DataFrame({"cocktail_id": cocktail_ids_list, "garnish_id": garnish_ids_list})

def populate_garnish_instructions_table(garnish_instructions_df):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for row in range(len(garnish_instructions_df)):
        cocktail_id = garnish_instructions_df.iloc[row, 0]
        garnish_id = garnish_instructions_df.iloc[row, 1]
        print(cocktail_id, garnish_id)
        sql = f"INSERT INTO Garnish_Instructions (Cocktail_ID, Garnish_ID) VALUES ('{cocktail_id}', '{garnish_id}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Garnish_Instructions")
    data = cursor.fetchall()
    print("++++++Garnish Ingredients Table Populated+++++++++")
    conn.close()
populate_garnish_instructions_table(garnish_ingredients_df)


####################
### RATING TABLE ###
####################
#set empty lists for cocktail ids and ratings
cocktail_ids_list = []
ratings_list = []
#for id in cocktail ids
for _id in cocktail_ids:
    #generate 5 random integers between 1 and 5 for each cocktail id
    for i in range(5):
        #append cocktial id and rating to lists
        cocktail_ids_list.append(_id)
        ratings_list.append(random.randint(1,5))

#create rating df
rating_df = pd.DataFrame({"rating": ratings_list, "cocktail_id": cocktail_ids_list})

def populate_rating_table(rating_df):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for row in range(len(rating_df)):
        rating = rating_df.iloc[row, 0]
        cocktail_id = rating_df.iloc[row, 1]
        print(rating)
        sql = f"INSERT INTO Ratings (Rating, Cocktail_ID) VALUES ('{rating}','{cocktail_id}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Ratings")
    data = cursor.fetchall()
    print("++++++Rating Table Populated++++++")
    conn.close()
populate_rating_table(rating_df)




print("connecting")

conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
cursor = conn.cursor()
cursor.execute('USE cocktailproject')
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
print(tables)
cursor.execute("SELECT * FROM Cocktails;")
cocktails = cursor.fetchall()
print(cocktails)
conn.close()
print("SUCCESS")