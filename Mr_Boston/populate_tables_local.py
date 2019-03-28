from credentials_local import user, password, rds_host
import pymysql
import pandas as pd
from boston_functions import *
import re
import numpy as np
from liquid import liquids
from garnish import garnishes

data = pd.read_csv("./mr-boston-all-glasses.csv")

data = data[data.loc[:, "glass-size"].notna()]

valid_units = ["oz", "tsp", "splash", "dash"]

fill_liquid = ["ginger ale", "carbonated water", "cola", "water", "chilled champagne", "soda water", 
               "club soda", "ginger ale or soda water", "lemon-lime soda", "ginger beer", "bitter lemon soda",
               "apple juice", "orange juice"]

invaild_ingredients = ['chopped', 'cut in half', 'cut in halves', 'cut into halves', 'flamed', 'hulled', 'long', 'skinned',
                       'whipped', "preferably b.a. reynold's", 'preferably jamaican', 'preferably japanese', 
                       'preferably pedro ximenez', "such as bittermen's elemakule", 'such as demerara', 
                       'such as islay or skye', 'such as nasturtium']

ingredient_indicies = range(3, 14)

all_recipies, measures = get_cocktail_recipies(data, ingredient_indicies, liquids, garnishes, invaild_ingredients, valid_units)

categories = list(set(data.iloc[:, 1])) + ["AI Instant Classic"]

liquid_colors = pd.read_csv("./LIquid_Colors_Final.csv")

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
    print(data)
    conn.close()

populate_liquid_table(liquid_colors)

def populate_garnish_table(garnishes):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for garnish in garnishes:
        sql = f"INSERT INTO Garnishes (Garnish_Name) VALUES ('{garnish}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Garnishes")
    data = cursor.fetchall()
    print(data)
    conn.close()

# populate_garnish_table(garnishes)

def populate_category_table(categories):
    conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
    cursor = conn.cursor()
    cursor.execute('USE cocktailproject')
    for category in categories:
        sql = f"INSERT INTO Categories (Category_Name) VALUES ('{category}');"
        cursor.execute(sql)
    conn.commit()
    cursor.execute("SELECT * FROM Categories")
    data = cursor.fetchall()
    print(data)
    conn.close()

# populate_category_table(categories)

glass_table_sql = "CREATE TABLE Glasses ( \
                    Glass_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                    , Glass_Name VARCHAR(24) \
                    , Glass_Size INT \
                    , Mask VARCHAR(900) \
                    , Path VARCHAR(3000) \
                    , Mask_Height FLOAT \
                    , Mask_Top_Margin FLOAT\
                    );"

cocktail_table_sql = "CREATE TABLE Cocktails ( \
                        Cocktail_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Cocktail_Name VARCHAR(80) \
                        , Glass_ID INT \
                        , Category_ID INT \
                        , FOREIGN KEY (Glass_ID) REFERENCES Glasses(Glass_ID) \
                        , FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID) \
                        );"

liquid_instructions_table_sql = "CREATE TABLE Liquid_Instuctions ( \
                                Liquid_Instruction_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                                , Cocktail_ID INT \
                                , Liquid_ID INT \
                                , Measure VARCHAR(24) \
                                , FOREIGN KEY (Cocktail_ID) REFERENCES Cocktails(Cocktail_ID) \
                                , FOREIGN KEY (Liquid_ID) REFERENCES Liquids(Liquid_ID) \
                                );"

garnish_instructions_table_sql = "CREATE TABLE Garnish_Instuctions ( \
                                    Garnish_Instruction_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                                    , Cocktail_ID INT \
                                    , Garnish_ID INT \
                                    , FOREIGN KEY (Cocktail_ID) REFERENCES Cocktails(Cocktail_ID) \
                                    , FOREIGN KEY (Garnish_ID) REFERENCES Garnishes(Garnish_ID) \
                                    );"

rating_table_sql = "CREATE TABLE Ratings ( \
                Rating_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                , Rating INT \
                , Cocktail_ID INT\
                , FOREIGN KEY (Cocktail_ID) REFERENCES Cocktails(Cocktail_ID) \
                );"



# print("connecting")
# def create_tables():
# conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
# cursor = conn.cursor()
# cursor.execute('USE cocktailproject')
# cursor.execute("SHOW TABLES;")
# tables = cursor.fetchall()
# cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
# for table in tables:
#     cursor.execute(f"DROP TABLE {table[0]};")
# cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
# for table in tables_to_create:
#     cursor.execute(table)
# cursor.execute("SHOW TABLES;")
# tables = cursor.fetchall()
# print(tables)
# cursor.execute("SELECT * FROM Cocktails;")
# tables = cursor.fetchall()
# print(tables)
# conn.close()
# print("success")

# create_tables()