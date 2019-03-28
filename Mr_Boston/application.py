# from flask import Flask, jsonify, request, redirect
# from flask_cors import CORS
from credentials import user, password, rds_reader, rds_writer
import pymysql



liquid_table_sql = "CREATE TABLE Liquids ( \
                        Ingredient_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Liquid_Name VARCHAR(80) \
                        , Color VARCHAR(10) \
                        );"

garnish_table_sql = "CREATE TABLE Garnishes ( \
                        Ingredient_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Garnish_Name VARCHAR(80) \
                        );"

measure_table_sql = "CREATE TABLE Measurements ( \
                        Measure_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , String_Measure VARCHAR(12) \
                        , Int_Measure FLOAT \
                        , Units VARCHAR(10) \
                        );"

glass_table_sql = "CREATE TABLE Glasses ( \
                    Glass_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                    , Glass_Name VARCHAR(24) \
                    , Glass_Size INT \
                    , Mask VARCHAR(900) \
                    , Path VARCHAR(3000) \
                    , Mask_Height FLOAT \
                    , Mask_Top_Margin \
                    );"

cocktail_table_sql = "CREATE TABLE Cocktails ( \
                        Cocktail_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Cocktail_Name VARCHAR(80) \
                        , Glass_ID INT \
                        , FOREIGN KEY (Glass_ID) REFERENCES Glasses(Glass_ID) \
                        );"

ingredients_table_sql = "CREATE TABLE Cocktails ( \
                        Cocktail_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Cocktail_Name VARCHAR(80) \
                        , Glass_ID INT \
                        , FOREIGN KEY (Glass_ID) REFERENCES Glasses(Glass_ID) \
                        );"



print("connecting")
# def create_tables():
conn = pymysql.connect(rds_writer, user=user, password=password, connect_timeout=50)
cursor = conn.cursor()
cursor.execute('USE cocktailproject')
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
for table in tables:
    cursor.execute(f"DROP TABLE {table[0]};")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

cursor.execute(liquid_table_sql)
cursor.execute(measure_table_sql)
cursor.execute(glass_table_sql)
cursor.execute(cocktail_table_sql)
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
print(tables)
cursor.execute("SELECT * FROM Cocktails;")
tables = cursor.fetchall()
print(tables)
conn.close()
print("success")

# create_tables()