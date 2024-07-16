import requests
from api_key import api_key
from url import url

def main():
    welcome()
   
def welcome():
    print("=============================================================================================================================================")
    print("Welcome to Know Nutrition")
    food_name = input("Write the name of food you want to know the nutrition of: ")
    print("=============================================================================================================================================")
    get_the_data(food_name)

# getting the data
def get_the_data(food_name):
    my_url = url
    params = {
        "query" : food_name,
        "api_key": api_key
    }
    response = requests.get(my_url,params=params)
    if response.status_code == 200:
        data = response.json()
    else:
        print("Error getting data from the source Sorry!")
    get_food_data_foundation(data)

def get_food_data_foundation(data):
    #getting all the food data which comes under Foundation data type from USDA DATABASE    
    foods = [food for food in data["foods"] if food["dataType"] == "Foundation"]
    description = [food["description"] for food in foods]

    #asking few questions   
    print(description)
    print()
    asking_description = input("choose from the list the description of the food by writing 1 for first item 2 for second one and so on: ")
    if int(asking_description) > len(description) or int(asking_description) < 0:
        raise Exception("Invalid item number!")
    print("=============================================================================================================================================")
    print_report(foods,description,asking_description)


def print_report(foods,description,asking_description):
    #printing information
    for food in foods:
        if food["description"] == description[int(asking_description) - 1]:
            print(food["description"])
            print()
        print("Do you want to know all the nutrion or some specific nutrion (eg protein)?")
        ask2 = input("write 'ALL' for all the nutrition or write 'SPECIFIC' if you want some specific nutrition: ")
        
        if ask2.lower() == 'all':
            print_all_nutrients(food)
            return
            
        elif ask2.lower() == 'specific':
            print_specific_nutrients(food)
            return
        else:
            print("invalid command!")
            break


def print_all_nutrients(food):
    for food_nutrient in food["foodNutrients"]:
        nutrient_name = food_nutrient["nutrientName"]
        nutrient_value = food_nutrient["value"]
        nutrient_value_unit = food_nutrient["unitName"]
        printing_string = f"{nutrient_name}, {nutrient_value} {nutrient_value_unit}"
        print("=========================================================================================================================================")
        print(printing_string)
    return
    
def print_specific_nutrients(food):
    nutrient_names = {}
    nutrient_value = []
    nutrient_value_unit = []
    i = 1
    for food_nutrient in food["foodNutrients"]:
        nutrient_names[i] = food_nutrient["nutrientName"]
        nutrient_value.append(food_nutrient["value"])
        nutrient_value_unit.append(food_nutrient["unitName"])
        i += 1
    print()
    print(nutrient_names)
    print() 
    specific_nutrient = input("choose from the list the specific nutrient of the food by writing 1 for first item 2 for second one and so on: ")
        
    if int(specific_nutrient) > len(nutrient_names) or int(specific_nutrient) < 0:
        raise Exception("Invalid item number!")
    else:
        printing_string = f"{nutrient_names[int(specific_nutrient)]}, {nutrient_value[int(specific_nutrient)-1]} {nutrient_value_unit[int(specific_nutrient)-1]}"
        print("=========================================================================================================================================")
        print(printing_string)
        print("=========================================================================================================================================")
        return
    
main()



