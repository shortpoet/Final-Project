import numpy as np
import re


def remove_leading_space(text):
    for char in text:
        if char != ' ':
            break
        else:
            text = text[1:]
    return text

#  remove = ['chopped',
#     'cut in half',
#     'cut in halves',
#     'cut into halves',
#     'flamed',
#     'hulled',
#     'long',
#     "preferably b.a. reynold's",
#     'preferably jamaican',
#     'preferably japanese',
#     'preferably pedro ximenez',
#     "such as bittermen's elemakule",
#     'such as demerara',
#     'such as islay or skye',
#     'such as nasturtium',
#     'skinned',
#     'whipped',
# ]

def mung_text(text):
    text = text.lower()
    text = remove_leading_space(text)
    text = text.replace("old mr. boston ", "")
    text = text.replace("mr. boston ", "")
    text = text.replace("juie", "juice")
    text = text.replace("pimm's no. 1 cup", "pimm's cup")
    text = text.replace("-flavored", " flavored")
    text = text.replace("calvados, apple brandy, or applejack", "apple brandy or applejack")
    text = text.replace(", such as laphroaig", "")
    if "juice of a" in text: 
        text = text.replace("juice of a ", "") + " juice"
    if "juice of " in text: 
        text = text.replace("juice of ", "") + " juice"
    text = text.replace("roses", "rose's")
    text = text.replace("100 proof", "100-proof")
    text = text.replace("  ", " ")
    return text


def split_on_comma(text):
    if text == 'nan':
        return []
    text_list = text.split(",")
    return [remove_leading_space(t) for t in text_list]

def vaild_ingredient(ingredient, valid_ingredients):
    for valid_ingredient in valid_ingredients:
        if valid_ingredient in ingredient:
            return True
    return False

def get_word_children(list_of_words):
    if len(list_of_words) == 0:
        return []
    else:
        children = []
        for child in list_of_words:
            for parent in list_of_words:
                if child != parent and child in parent:
                    children.append(child)
        children = list(set(children))
        parents = []
        for word in list_of_words:
            if word not in children:
                parents.append(word)
        parents = list(set(parents))
        return [parents] + get_word_children(children)

def adjust_measurement(measurement):
    items = measurement.split(' ')
    final = ''
    amount = 0
    for item in items:
        try:
            amount += eval(item)
        except:
            final += f"{item} "
    if amount > 0:
        final = f"{round(amount, 2)} " + final
    return final[:-1]

def get_cocktail_recipies(dataframe, ingredient_indicies, liquid_list, garnish_list, invaild_ingredients, valid_units):

    all_recipies = []
    measures = []
    
    liquid_generational = get_word_children(liquid_list)
    garnish_generational = get_word_children(garnish_list)
    
    # For each row in the data
    for row in range(len(dataframe)):
        
        name = dataframe.iloc[row, 0]
        category = dataframe.iloc[row, 1]
        instructions = dataframe.iloc[row, 14]
        glass = dataframe.iloc[row, 15]
        glass_size = get_size(dataframe.iloc[row, 16])
        drink_recipe = []
        
        # Pull out the ingredients and their measurements
        for ingredient_index in ingredient_indicies:

            # Ingredients
            ingredients = mung_text(str(dataframe.iloc[row, ingredient_index]))
            ingredient_list = split_on_comma(ingredients)

            # Potential Measure for that ingredient
            measure = str(dataframe.iloc[row, ingredient_index - 1])
            valid_measure = False
            if len(measure) < 10:
                for unit in valid_units:
                    if unit in measure:
                        valid_measure = True
                        
#             if not valid_measure and measure[0] in [str(n) for n in range(10)]:
#                 valid_measure = True
#                 print(measure)
#                 measure = str(measure[0]) + " oz*"
#                 print(measure)
                
            if valid_measure:
                measures.append(measure)
                
            else:
                measure = "fill"

            # Find ingredient type must start at most complecated and move to least
            # Some garnishes like raspberry appear in liquids => liquids first
            for ingredient in ingredient_list:
                
                # Ignore invaild data
                if ingredient in invaild_ingredients:
                    pass
                
                else:
                    
                    # Try Liquid
                    recorded_ingredient = find_ingredient(ingredient, liquid_generational)
                    ingredient_type = "liquid"
                    
                    if recorded_ingredient is None:
                        
                        # Try Garnish
                        recorded_ingredient = find_ingredient(ingredient, garnish_generational)
                        ingredient_type = "garnish"
                        
                    if recorded_ingredient is None:
                        # Missed a bad ingredient pass
                        pass
                    
                    else:
                        if ingredient_type == "garnish":
                            # no need for measure
                            drink_recipe += [["add", recorded_ingredient]]
                        else:
                            drink_recipe += [[measure, recorded_ingredient]]
                            
        drink_info = {"name": name,
                      "category": category,
                      "instructions": instructions,
                      "glass": glass,
                      "glass_size": glass_size,
                      "recipe": drink_recipe}
        all_recipies.append(drink_info)
        
    return all_recipies, measures


def find_ingredient(ingredient, ingredient_lists):
    returned_ingredient = None
    for ingredient_list in ingredient_lists:
        for possible_match in ingredient_list:
            if ingredient in possible_match:
                returned_ingredient = possible_match
                break
        if returned_ingredient is not None:
            break
    return returned_ingredient

def get_size(string):
    string = remove_leading_space(string)
    num = ""
    for char in string:
        if char in [str(n) for n in range(10)]:
            num += char
        elif len(num) > 0:
            return eval(num)
    return string