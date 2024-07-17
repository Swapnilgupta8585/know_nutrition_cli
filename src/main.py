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
    try:
        get_the_data(food_name)
    except Exception as e:
        print(f'ERROR: {e}')
    print("=============================================================================================================================================")


# getting the data through the USDA API From USDA Database
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
        raise Exception("Sorry, can't fetch the data right now!")
    get_food_data_foundation(data)


def get_food_data_foundation(data):
    #getting all the food data which comes under Foundation data type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "Foundation"]

    #if no data in Foundation data type try to find data from SR Legacy data type
    if len(foods) == 0:
        get_food_data_SR_legacy(data)
        return
    #else if found some data call print_description_of_foods function
    print_description_of_foods(foods)


def get_food_data_SR_legacy(data):
    #getting all the food data which comes under SR Legacy data type from USDA DATABASE    
    foods = [food for food in data["foods"] if food["dataType"] == "SR Legacy"]

    #if no data in SR Legacy data type try to find data from Survey_FNDDS data type
    if len(foods) == 0:
        get_food_data_Survey_FNDDS_(data)
        return
    #else if found some data call print_description_of_foods 
    print_description_of_foods(foods)


def get_food_data_Survey_FNDDS_(data):
    #getting all the food data which comes under Survey_FNDDS data type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "Survey (FNDDS)"]

    #if no data in Survey_FNDDS type ask some questions whether they want to know from Branded data type or not
    if len(foods) == 0:
        print("hey we don't have this food in our database!")
        print("want to know the nutrition through products which different brand offers")
        ask = input("write 1->YES or 0-> NO: ")

        if int(ask) == 1:
                get_food_data_Branded(data)
                return
        
        elif int(ask) == 0:
            return
        
        else:
            raise Exception("invalid command")
    
    #else if found some data call print_description_of_foods function
    print_description_of_foods(foods)

def get_food_data_Branded(data):
    #getting all the food data which comes under Foundation data type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "Branded"]
    
    if len(foods) == 0:
        print("Sorry, can't find the data for this food")
        return
        
    #else if found some data call print_description_of_foods function
    print_description_of_foods(foods)


def print_description_of_foods(foods):
    description = {}
    i = 1
    for food in foods:
        description[i] = food["description"]
        i += 1
    
    for key,value in description.items():
        print(f"{key}: {value}")
    print()

    #asking few questions  
    description_num = input("choose from the list the description of the food by writing 1 for first item 2 for second one and so on: ")

    #checking if the input given is valid or not
    if int(description_num) > len(description) or int(description_num) < 0:
        raise Exception("Invalid item number!")
    print("=============================================================================================================================================")
    print_report(foods,description,description_num)


def print_report(foods,description,description_num):
    #printing information
    for food in foods:
        if food["description"] == description[int(description_num)]:
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
            raise Exception("invalid command")


def print_all_nutrients(food):
    for food_nutrient in food["foodNutrients"]:
        nutrient_name = food_nutrient["nutrientName"]
        nutrient_value = food_nutrient["value"]
        nutrient_value_unit = food_nutrient["unitName"]
        printing_string = f"{nutrient_name}, {nutrient_value} {nutrient_value_unit}"
        print("=========================================================================================================================================")
        print(printing_string)
    
    

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
    for key,value in nutrient_names.items():
        print(f"{key}: {value}")
    print()
    
    specific_nutrient = input("choose from the list the specific nutrient of the food by writing 1 for first item 2 for second one and so on: ")
        
    if int(specific_nutrient) > len(nutrient_names) or int(specific_nutrient) < 0:
        raise Exception("Invalid item number!")
    else:
        printing_string = f"{nutrient_names[int(specific_nutrient)]}, {nutrient_value[int(specific_nutrient)-1]} {nutrient_value_unit[int(specific_nutrient)-1]}"
        print("=========================================================================================================================================")
        print(printing_string)
        
main()



