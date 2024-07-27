import requests
import time
import sys
import signal
import pyfiglet
from api_key import api_key
from url import url
from terminaltexteffects.effects.effect_waves import Waves
from terminaltexteffects.effects.effect_wipe import Wipe
from terminaltexteffects.effects.effect_expand import Expand
from terminaltexteffects.effects.effect_burn import Burn
from tabulate import tabulate


def main():
    # set up signal handling
    signal.signal(signal.SIGINT, handle_exit)
    print_big("KNOW NUTRITION", wave_animation)

    try:
        welcome()
    except KeyboardInterrupt:
        # if keyboard interrupt(SIGINT-> Ctrl + C) occurs call handle_exit()
        handle_exit(signal.SIGINT, None)


def welcome():
    # initial welcome message
    wipe_animation("""Welcome to Know Nutrition, a program that tells you the different nutritional values of foods.
                    To exit the program simply press [ctrl + C]""")
    wipe_animation("FOOD NAME:")
    food_name = input("-> ")
    expand_animation("===========================================================================================================================")
    print("getting the data...")

    # get the data about food_name
    get_the_data(food_name)


#if CTRL + C interrupt occurs, exit the program
def handle_exit(signal_received, frame):
    expand_animation("===========================================================================================================================")
    print_big("End!", burn_animation)
    expand_animation("===========================================================================================================================")
    sys.exit(0)


#printing big text using pyfiglet module of python
def print_big(word, printing_func):
    text = pyfiglet.figlet_format(word)
    printing_func(text)


# terminal_text_effect animation function
def wave_animation(word):
    effect = Waves(word)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)


# terminal_text_effect animation function
def burn_animation(word):
    effect = Burn(word)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)


# terminal_text_effect animation functions
def wipe_animation(word):
    effect = Wipe(word)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)


# terminal_text_effect animation functions
def expand_animation(word):
    effect = Expand(word)
    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)


def get_the_data(food_name):
    my_url = url
    params = {"query": food_name, "api_key": api_key}

    # get the data through the USDA API From USDA Database
    response = requests.get(my_url, params=params)

    # if success, Deserialize the JSON data to Python dictionary
    if response.status_code == 200:
        data = response.json()

        # call get_food_data_foundation() to get the food data
        get_food_data_foundation(data)
    else:
        raise Exception("Sorry, can't fetch the data right now!")


def get_food_data_foundation(data):
    # get all the food data which comes under Foundation data type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "Foundation"]

    # if no data is found in Foundation data type, try to find data from SR Legacy data type
    if len(foods) == 0:
        get_food_data_SR_legacy(data)
        return
    # if found some data in Foundation data type, call print_description_of_foods()
    print_description_of_foods(foods)


def get_food_data_SR_legacy(data):
    # get all the food data which comes under SR Legacy data type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "SR Legacy"]

    # if no data is found in SR Legacy data type try to find data from Survey_FNDDS data type
    if len(foods) == 0:
        get_food_data_Survey_FNDDS(data)
        return

    # if found some data in SR Legacy data type, call print_description_of_foods()
    print_description_of_foods(foods)


def get_food_data_Survey_FNDDS(data):
    # get all the food data which comes under Survey_FNDDS data type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "Survey (FNDDS)"]

    # if no data is found in Survey_FNDDS data type ask some questions
    if len(foods) == 0:
        wipe_animation("Sorry, we couldn't find data for this food.")
        expand_animation("===========================================================================================================================")
        ask_for_branded_food(data)
        return
    
    # if found some data in Survey_FNDDS data type, call print_description_of_foods function
    print_description_of_foods(foods)


def ask_for_branded_food(data):
    # asking whether to find the data from branded data type or not
    wipe_animation("Want to know the nutrition of this food if a brand offers it? Enter 1 for YES or 0 for NO")
    # wipe_animation("Enter 1 for YES or 0 for NO")
    ask = input("-> ")
    expand_animation("===========================================================================================================================")
    
    try:
        # if yes, call get_food_data_Branded()
        if int(ask) == 1:
            get_food_data_Branded(data)
            return

        # if no, just restart the program
        elif int(ask) == 0:
            time.sleep(1)
            ask_want_to_restart()

        else:
            raise ValueError("invalid input!")

    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        ask_for_branded_food(data)


def get_food_data_Branded(data):
    # get all the food data which comes under Branded type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "Branded"]

    if len(foods) == 0:
        wipe_animation("Sorry, we couldn't find data for this food.")
        expand_animation("===========================================================================================================================")
        ask_want_to_restart()

    # if found some data in Branded data type, call print_description_of_foods function
    else:
        print_description_of_foods(foods, True)


def print_slowly(text,delay):
    for char in text:
        print(char,end='',flush=True)
        time.sleep(delay)
    print()


def print_description_of_foods(foods, is_branded_food=False):
    # get all the food description
    description = {}
    i = 1
    for food in foods:
        description[i] = food["description"]
        i += 1

    table_data = [[key, value] for key, value in description.items()]
    table = tabulate(
        table_data, headers=["S.NO", "DESCRIPTION OF FOOD"], tablefmt="fancy_grid"
    )
    print_slowly(table,0.0005)
    expand_animation("===========================================================================================================================")

    # ask for the food's discription number
    ask_description_num(description, foods, is_branded_food)


def ask_description_num(description, foods, is_branded_food):
    # asking few questions
    wipe_animation("Select a food item by entering its number: 1 for the first, 2 for the second, etc.")
    description_num = input("-> ")
    expand_animation("===========================================================================================================================")

    # checking if the input given is valid or not
    try:
        if int(description_num) > len(description) or int(description_num) <= 0:
            raise ValueError("invalid item number!")

        # if everthing is okay call print_report() on selected food
        print_the_data(foods, description, description_num, is_branded_food)
        return

    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        ask_description_num(description, foods, is_branded_food)


def print_the_data(foods, description, description_num, is_branded_food):
    for food in foods:
        if food["description"] == description[int(description_num)]:
            wipe_animation("Enter 'a' for complete nutritional information or 's' for selected nutrients.")
            ask2 = input("-> ")
            expand_animation("===========================================================================================================================")

            try:
                if ask2.lower() == "a":
                    is_branded_food_data_type(food, is_branded_food)
                    print_all_nutrients(food)
                    return
                elif ask2.lower() == "s":
                    is_branded_food_data_type(food, is_branded_food)
                    print_specific_nutrients(food)
                    return
                else:
                    raise ValueError("invalid input!")

            except ValueError:
                wipe_animation("Invalid input! Please enter a valid option.")
                expand_animation("===========================================================================================================================")
                print_the_data(foods, description, description_num, is_branded_food)


def is_branded_food_data_type(food, is_branded_food):
    if is_branded_food:
        table_data = []
        table_data.append(['Description',food["description"]])
        table_data.append(['Brand Name',food["brandName"]])
        table_data.append(['Food Category',food["foodCategory"]])
        table_data.append(['Package Weight',food["packageWeight"]])
        table_data.append(['Serving Size','100g'])

        table = tabulate(table_data, headers=['About','Value'],tablefmt="fancy_grid")
        print_slowly(table,0.0001)
    return


def print_all_nutrients(food):
    expand_animation("==========================================================================================================================")
    wipe_animation("COMPLETE NUTRITIONAL VALUE")
    print()
    nutrient_name = []
    nutrient_value = []
    for food_nutrient in food["foodNutrients"]:
        nutrient_name.append(food_nutrient["nutrientName"])
        nutrient_value.append(f'{food_nutrient["value"]}{food_nutrient["unitName"]}')

    table_data = list(zip(nutrient_name,nutrient_value))
    table = tabulate(table_data,headers=['NUTRIENT NAME','VALUE/100g'],tablefmt="fancy_grid")
    print_slowly(table,0.0005)
    expand_animation("==========================================================================================================================")
    ask_want_to_restart()


def print_specific_nutrients(food):
    expand_animation("==========================================================================================================================")
    wipe_animation("COMPLETE NUTRITIONAL VALUE")
    print()
    
    nutrient_names = {}
    nutrient_value = []
    nutrient_value_unit = []
    i = 1
    for food_nutrient in food["foodNutrients"]:
        nutrient_names[i] = food_nutrient["nutrientName"]
        nutrient_value.append(food_nutrient["value"])
        nutrient_value_unit.append(food_nutrient["unitName"])
        i += 1

    table_data = [[key, value] for key, value in nutrient_names.items()]
    table = tabulate(
        table_data, headers=["S.NO", "NUTRIENT NAME"], tablefmt="fancy_grid"
    )
    print_slowly(table,0.0005)
    expand_animation("===========================================================================================================================")

    ask_specific_nutrient_num(food, nutrient_names, nutrient_value, nutrient_value_unit)


def ask_specific_nutrient_num(food, nutrient_names, nutrient_value, nutrient_value_unit):
    wipe_animation("Select the specific nutrient by entering its number: 1 for the first, 2 for the second, etc.")
    specific_nutrient_num = input("-> ")
    expand_animation("===========================================================================================================================")

    # checking if the input given is valid or not
    try:
        if (
            int(specific_nutrient_num) > len(nutrient_names)
            or int(specific_nutrient_num) <= 0
        ):
            raise ValueError("invalid item number!")

        # if everthing is okay
        printing_string = f"{nutrient_names[int(specific_nutrient_num)]}, {nutrient_value[int(specific_nutrient_num)-1]}{nutrient_value_unit[int(specific_nutrient_num)-1].lower()}"
        wave_animation(f'{printing_string} in 100g')
        expand_animation("===========================================================================================================================")
        ask_want_to_know_more(food, nutrient_names, nutrient_value, nutrient_value_unit)

    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        ask_specific_nutrient_num(
            food, nutrient_names, nutrient_value, nutrient_value_unit
        )


def ask_want_to_know_more(food, nutrient_names, nutrient_value, nutrient_value_unit):
    wipe_animation("Want to see more specific nutritional values for this food? Enter 1 for YES or 0 for NO")
    # wipe_animation("Enter 1 for YES or 0 for NO")
    ask = input("-> ")
    expand_animation("===========================================================================================================================")
    try:
        # if yes, call get_food_data_Branded()
        if int(ask) == 1:
            ask_specific_nutrient_num(
                food, nutrient_names, nutrient_value, nutrient_value_unit
            )
            return

        # if no, just restart the program
        elif int(ask) == 0:
            time.sleep(1)
            ask_want_to_restart()
            return

        else:
            raise ValueError("invalid input!")

    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        ask_want_to_know_more(food, nutrient_names, nutrient_value, nutrient_value_unit)


def ask_want_to_restart():
    wipe_animation("Do you want to check the nutritional values for other foods? Enter 1 for YES or 0 for NO")

    # wipe_animation("Enter 1 for YES or 0 for NO")
    ask = input("-> ")
    expand_animation("===========================================================================================================================")

    try:
        # if yes, call get_food_data_Branded()
        if int(ask) == 1:
            welcome()

        # if no, just restart the program
        elif int(ask) == 0:
            time.sleep(1)
            print_big("END", burn_animation)
            expand_animation("===========================================================================================================================")
            return

        else:
            raise ValueError("invalid input!")

    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        ask_want_to_restart()


main()
