from credentials_local import user, password, rds_host
import pymysql


liquid_table_sql = "CREATE TABLE Liquids ( \
                        Liquid_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Liquid_Name VARCHAR(80) \
                        , Color VARCHAR(10) \
                        );"

garnish_table_sql = "CREATE TABLE Garnishes ( \
                        Garnish_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Garnish_Name VARCHAR(80) \
                        );"

category_table_sql = "CREATE TABLE Categories ( \
                        Category_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                        , Category_Name VARCHAR(80) \
                        );"

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
                        , Instructions VARCHAR(500) \
                        , FOREIGN KEY (Glass_ID) REFERENCES Glasses(Glass_ID) \
                        , FOREIGN KEY (Category_ID) REFERENCES Categories(Category_ID) \
                        );"

liquid_instructions_table_sql = "CREATE TABLE Liquid_Instructions ( \
                                Liquid_Instruction_ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT \
                                , Cocktail_ID INT \
                                , Liquid_ID INT \
                                , Measure VARCHAR(24) \
                                , Measure_Float FLOAT \
                                , FOREIGN KEY (Cocktail_ID) REFERENCES Cocktails(Cocktail_ID) \
                                , FOREIGN KEY (Liquid_ID) REFERENCES Liquids(Liquid_ID) \
                                );"

garnish_instructions_table_sql = "CREATE TABLE Garnish_Instructions ( \
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


tables_to_create = [liquid_table_sql, garnish_table_sql, category_table_sql, 
                    glass_table_sql, cocktail_table_sql, liquid_instructions_table_sql, 
                    garnish_instructions_table_sql, rating_table_sql]

print("connecting")

conn = pymysql.connect(rds_host, user=user, password=password, connect_timeout=50)
cursor = conn.cursor()
# create database
sql = "CREATE DATABASE IF NOT EXISTS cocktailproject"
cursor.execute(sql)
cursor.execute('USE cocktailproject')
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
for table in tables:
    cursor.execute(f"DROP TABLE {table[0]};")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
for table in tables_to_create:
    cursor.execute(table)
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()
print(tables)
cursor.execute("SELECT * FROM Cocktails;")
cocktails = cursor.fetchall()
print(cocktails)
conn.close()
print("success")