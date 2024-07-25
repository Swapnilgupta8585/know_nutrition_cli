import requests
import time
from api_key import api_key
from url import url
from terminaltexteffects.effects.effect_waves import Waves
from terminaltexteffects.effects.effect_wipe import Wipe
from terminaltexteffects.effects.effect_expand import Expand
from tabulate import tabulate

def main():
    welcome()


# terminal_text_effect animation function
def wave_animation(word):
    effect = Waves(word)
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


def welcome():
    # initial welcome message
    wave_animation(
        "Welcome to Know Nutrition, A program which tells the different nurtition value of a food"
    )
    wipe_animation("FOOD NAME:")
    food_name = input("-> ")
    expand_animation(
        "==========================================================================================================================="
    )
    print("getting the data...")

    # get the data about food_name
    get_the_data(food_name)


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
    foods = [food for food in data["foods"]
             if food["dataType"] == "Foundation"]

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
    foods = [food for food in data["foods"]
             if food["dataType"] == "Survey (FNDDS)"]

    # if no data is found in Survey_FNDDS data type ask some questions
    if len(foods) == 0:
        wipe_animation("Sorry can't find the data for this food")
        expand_animation(
            "==========================================================================================================================="
        )
        ask_for_branded_food(data)
        return
    # if found some data in Survey_FNDDS data type, call print_description_of_foods function
    print_description_of_foods(foods)


def ask_for_branded_food(data):
    # asking whether to find the data from branded data type or not
    wipe_animation(
        "Want to know the nutrition through products which different brand offers?"
    )

    wipe_animation("write 1->YES or 0-> NO: ")
    ask = input("-> ")
    expand_animation(
        "==========================================================================================================================="
    )
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
        wipe_animation(
            "Invalid item number or input! Please enter a valid number.")
        expand_animation(
            "==========================================================================================================================="
        )
        ask_for_branded_food(data)


def get_food_data_Branded(data):
    # get all the food data which comes under Branded type from USDA DATABASE
    foods = [food for food in data["foods"] if food["dataType"] == "Branded"]

    if len(foods) == 0:
        wipe_animation("Sorry, can't find the data for this food")
        expand_animation(
            "==========================================================================================================================="
        )
        ask_want_to_restart()

    # if found some data in Branded data type, call print_description_of_foods function
    else:
        print_description_of_foods(foods, True)


def print_description_of_foods(foods, is_branded_food=False):
    # get all the food description
    description = {}
    i = 1
    for food in foods:
        description[i] = food["description"]
        i += 1

    # if length is more than 10 then just print the description of food else the animation will take a lot of time
    if len(description) > 6:
        table_data = [[key,value] for key,value in description.items()]
        table = tabulate(table_data,headers=["S.NO","DESCRIPTION"],tablefmt="fancy_grid")
        print(table)

    # else print the data with wipe_animation()
    else:
        for key, value in description.items():
            wipe_animation(f"{key}: {value}")

    expand_animation(
        "==========================================================================================================================="
    )
    # ask for the food's discription number
    ask_description_num(description, foods, is_branded_food)


def ask_description_num(description, foods, is_branded_food):
    # asking few questions
    wipe_animation(
        "choose from the list the description number of the food by writing 1 for the first item or 2 for second one and so on:"
    )
    description_num = input("-> ")
    expand_animation(
        "==========================================================================================================================="
    )

    # checking if the input given is valid or not
    try:
        if int(description_num) > len(description) or int(description_num) <= 0:
            raise ValueError("invalid item number!")

        # if everthing is okay call print_report() on selected food
        print_report(foods, description, description_num, is_branded_food)

    except ValueError:
        wipe_animation(
            "Invalid item number or input! Please enter a valid number.")
        expand_animation(
            "==========================================================================================================================="
        )
        ask_description_num(description, foods, is_branded_food)


def print_report(foods, description, description_num, is_branded_food):
    for food in foods:
        if food["description"] == description[int(description_num)]:
            wipe_animation(food["description"])
            expand_animation(
                "==========================================================================================================================="
            )
        wipe_animation(
            "write 'ALL' for all the nutrition or write 'SPECIFIC' if you want some specific nutrition: "
        )
        ask2 = input("-> ")
        expand_animation(
            "==========================================================================================================================="
        )

        try:
            if ask2.lower() == "all":
                is_branded_food_data_type(food, is_branded_food)
                print_all_nutrients(food)
                return
            elif ask2.lower() == "specific":
                is_branded_food_data_type(food, is_branded_food)
                print_specific_nutrients(food)
                return
            else:
                raise ValueError("invalid input!")

        except ValueError:
            wipe_animation("invalid input")
            expand_animation(
                "==========================================================================================================================="
            )
            print_report(foods, description, description_num, is_branded_food)


def is_branded_food_data_type(food, is_branded_food):
    if is_branded_food:
        wipe_animation(
            f'description: {food["description"]}\n'
            f'brandOwner: {food["brandOwner"]}\n'
            f'brandName: {food["brandName"]}\n'
            f'ingredients: {food["ingredients"]}\n'
            f'foodCategory: {food["foodCategory"]}\n'
            f'packageWeight: {food["packageWeight"]}\n'
        )

        serving_size = food["servingSize"]
        serving_size_unit = food["servingSizeUnit"]
        print(f"servingSize: {serving_size}{serving_size_unit}")
        print()
    return


def print_all_nutrients(food):
    if len(food["foodNutrients"]) > 10:
        print_all_nutrients_accordingly(food, print)

    else:
        print_all_nutrients_accordingly(food, wipe_animation)

    ask_want_to_restart()


def print_all_nutrients_accordingly(food, printing_func):
    for food_nutrient in food["foodNutrients"]:
        nutrient_name = food_nutrient["nutrientName"]
        nutrient_value = food_nutrient["value"]
        nutrient_value_unit = food_nutrient["unitName"]
        printing_string = f"{nutrient_name}, {nutrient_value} {nutrient_value_unit}"
        printing_func(printing_string)
        print("=========================================================================================================================================")


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

    if len(nutrient_names) > 6:
        # for key, value in nutrient_names.items():
        #     print(f"{key}: {value}")

        table_data = [[key,value] for key,value in nutrient_names.items()]
        table = tabulate(table_data, headers=["S.NO","NUTRIENT NAME"],tablefmt="fancy_grid")
        print(table)
    else:
        for key, value in nutrient_names.items():
            wipe_animation(f"{key}: {value}")
    expand_animation(
        "==========================================================================================================================="
    )

    ask_specific_nutrient_num(food, nutrient_names,
                              nutrient_value, nutrient_value_unit)


def ask_specific_nutrient_num(
    food, nutrient_names, nutrient_value, nutrient_value_unit
):
    wipe_animation(
        "choose from the list the specific nutrient of the food by writing 1 for first item 2 for second one and so on: "
    )
    specific_nutrient_num = input("-> ")
    expand_animation(
        "==========================================================================================================================="
    )

    # checking if the input given is valid or not
    try:
        if (
            int(specific_nutrient_num) > len(nutrient_names)
            or int(specific_nutrient_num) <= 0
        ):
            raise ValueError("invalid item number!")

        # if everthing is okay
        printing_string = f"{nutrient_names[int(specific_nutrient_num)]}, {nutrient_value[int(specific_nutrient_num)-1]} {nutrient_value_unit[int(specific_nutrient_num)-1]}"
        wave_animation(printing_string)
        expand_animation(
            "==========================================================================================================================="
        )
        ask_want_to_know_more(food, nutrient_names,
                              nutrient_value, nutrient_value_unit)

    except ValueError:
        wipe_animation(
            "Invalid item number or input! Please enter a valid number.")
        expand_animation(
            "==========================================================================================================================="
        )
        ask_specific_nutrient_num(
            food, nutrient_names, nutrient_value, nutrient_value_unit
        )


def ask_want_to_know_more(food, nutrient_names, nutrient_value, nutrient_value_unit):
    wipe_animation(
        "Want to know more specific nutritional values of this food?")

    wipe_animation("write 1->YES or 0-> NO: ")
    ask = input("-> ")
    expand_animation(
        "==========================================================================================================================="
    )
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

        else:
            raise ValueError("invalid input!")

    except ValueError:
        wipe_animation(
            "Invalid item number or input! Please enter a valid number.")
        expand_animation(
            "==========================================================================================================================="
        )
        ask_want_to_know_more(food, nutrient_names,
                              nutrient_value, nutrient_value_unit)


def ask_want_to_restart():
    wipe_animation("Want to restart the program")

    wipe_animation("write 1->YES or 0-> NO: ")
    ask = input("-> ")
    expand_animation(
        "==========================================================================================================================="
    )
    try:
        # if yes, call get_food_data_Branded()
        if int(ask) == 1:
            welcome()

        # if no, just restart the program
        elif int(ask) == 0:
            time.sleep(1)
            wave_animation("END OF PROGRAM!")
            expand_animation(
                "==========================================================================================================================="
            )
            return

        else:
            raise ValueError("invalid input!")

    except ValueError:
        wipe_animation(
            "Invalid item number or input! Please enter a valid number.")
        expand_animation(
            "==========================================================================================================================="
        )
        ask_want_to_restart()


main()
