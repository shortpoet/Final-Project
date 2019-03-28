from boston_functions import *
import pandas as pd
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

print(all_recipies)
