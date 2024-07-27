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
    # Set up signal handler for graceful exit on CTRL+C
    signal.signal(signal.SIGINT, handle_exit)
    
    # Print the program title with a wave animation
    print_big("KNOW NUTRITION", wave_animation)

    try:
        # Start the main program flow
        welcome()
    except KeyboardInterrupt:
        # Handle a KeyboardInterrupt exception (CTRL+C) gracefully
        handle_exit(signal.SIGINT, None)


def welcome():
    # Display a welcome message with animation and instructions for exiting
    wipe_animation("""Welcome to Know Nutrition, a program that tells you the different nutritional values of foods.
                    To exit the program simply press [ctrl + C]""")
    
    # Prompt the user to enter the food name
    wipe_animation("FOOD NAME:")
    food_name = input("-> ")
    expand_animation("===========================================================================================================================")
    
    # Indicate that data retrieval is in progress
    print("getting the data...")
    
    # Fetch the food data based on the user input
    get_the_data(food_name)


def handle_exit(signal_received, frame):
    # Handle the program exit when a termination signal is received (e.g., ctrl + C)
    expand_animation("===========================================================================================================================")
    # Print a big "End!" message with a burn animation
    print_big("End!", burn_animation)
    expand_animation("===========================================================================================================================")
    # Exit the program
    sys.exit(0)


def print_big(word, printing_func):
    # Format the given word into a large ASCII art text
    text = pyfiglet.figlet_format(word)
    # Print the ASCII art text using the provided printing function
    printing_func(text)


def wave_animation(word):
    # Create a Waves effect instance with the given word
    effect = Waves(word)
    # Use the effect's terminal output context
    with effect.terminal_output() as terminal:
        # Print each frame of the animation
        for frame in effect:
            terminal.print(frame)


def burn_animation(word):
    # Create a Burn effect instance with the given word
    effect = Burn(word)
    # Use the effect's terminal output context
    with effect.terminal_output() as terminal:
        # Print each frame of the animation
        for frame in effect:
            terminal.print(frame)


def wipe_animation(word):
    # Create a Wipe effect instance with the given word
    effect = Wipe(word)
    # Use the effect's terminal output context
    with effect.terminal_output() as terminal:
        # Print each frame of the animation
        for frame in effect:
            terminal.print(frame)


def expand_animation(word):
    # Create an Expand effect instance with the given word
    effect = Expand(word)
    # Use the effect's terminal output context
    with effect.terminal_output() as terminal:
        # Print each frame of the animation
        for frame in effect:
            terminal.print(frame)


def get_the_data(food_name):
    # Define the URL and parameters for the USDA API request
    my_url = url
    params = {"query": food_name, "api_key": api_key}

    # Make a GET request to the USDA API
    response = requests.get(my_url, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        # Deserialize the JSON data into a Python dictionary
        data = response.json()

        # Call get_food_data_foundation() to process the food data
        get_food_data_foundation(data)
    else:
        # Raise an exception if the data could not be fetched
        raise Exception("Sorry, can't fetch the data right now!")


def get_food_data_foundation(data):
    # Filter out foods that are of type 'Foundation' from the provided data
    foods = [food for food in data["foods"] if food["dataType"] == "Foundation"]

    # If no data of type 'Foundation' is found, try to find data from 'SR Legacy' type
    if len(foods) == 0:
        get_food_data_SR_legacy(data)
        return
    
    # If data of type 'Foundation' is found, display the food descriptions
    print_description_of_foods(foods)


def get_food_data_SR_legacy(data):
    # Filter out foods that are of type 'SR Legacy' from the provided data
    foods = [food for food in data["foods"] if food["dataType"] == "SR Legacy"]

    # If no data of type 'SR Legacy' is found, try to find data from 'Survey (FNDDS)' type
    if len(foods) == 0:
        get_food_data_Survey_FNDDS(data)
        return

    # If data of type 'SR Legacy' is found, display the food descriptions
    print_description_of_foods(foods)


def get_food_data_Survey_FNDDS(data):
    # Filter out foods that are of type 'Survey (FNDDS)' from the provided data
    foods = [food for food in data["foods"] if food["dataType"] == "Survey (FNDDS)"]

    # If no data of type 'Survey (FNDDS)' is found, inform the user and ask for branded food data
    if len(foods) == 0:
        wipe_animation("Sorry, we couldn't find data for this food.")
        expand_animation("===========================================================================================================================")
        ask_for_branded_food(data)
        return
    
    # If data of type 'Survey (FNDDS)' is found, display the food descriptions
    print_description_of_foods(foods)


def ask_for_branded_food(data):
    # Prompt the user to decide whether to look for branded food data
    wipe_animation("Want to know the nutrition of this food if a brand offers it? Enter 1 for YES or 0 for NO")
    # Get the user's input
    ask = input("-> ")
    expand_animation("===========================================================================================================================")
    
    try:
        # If the user enters 1, call the function to get branded food data
        if int(ask) == 1:
            get_food_data_Branded(data)
            return

        # If the user enters 0, restart the program
        elif int(ask) == 0:
            time.sleep(1)
            ask_want_to_restart()

        # Raise an exception if the input is not 1 or 0
        else:
            raise ValueError("invalid input!")

    # Handle the exception for invalid input
    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        # Prompt the user again
        ask_for_branded_food(data)


def get_food_data_Branded(data):
    # Filter out foods that are of type 'Branded' from the provided data
    foods = [food for food in data["foods"] if food["dataType"] == "Branded"]

    # Check if any branded food data was found
    if len(foods) == 0:
        # Inform the user if no branded food data was found and restart the program
        wipe_animation("Sorry, we couldn't find data for this food.")
        expand_animation("===========================================================================================================================")
        ask_want_to_restart()

    # If branded food data was found, display the food descriptions
    else:
        print_description_of_foods(foods, True)


def print_slowly(text, delay):
    # Iterate through each character in the text
    for char in text:
        # Print each character without moving to a new line
        # `end=''` ensures characters are printed on the same line
        # `flush=True` forces the output to be written immediately
        print(char, end='', flush=True)
        
        # Pause for the specified delay before printing the next character
        time.sleep(delay)
    
    # Print a newline character to move to the next line after the text is fully printed
    print()


def print_description_of_foods(foods, is_branded_food=False):
    # Get all the food descriptions
    description = {}
    i = 1
    for food in foods:
        description[i] = food["description"]
        i += 1

    # Prepare the data for displaying in a table format
    table_data = [[key, value] for key, value in description.items()]
    
    # Create a table using the tabulate library
    table = tabulate(
        table_data, headers=["S.NO", "DESCRIPTION OF FOOD"], tablefmt="fancy_grid"
    )
    
    # Print the table slowly for better visual effect
    print_slowly(table, 0.0005)
    
    # Display an animation to indicate the end of the description section
    expand_animation("===========================================================================================================================")

    # Ask for the food's description number
    ask_description_num(description, foods, is_branded_food)


def ask_description_num(description, foods, is_branded_food):
    # Ask the user to select a food item by entering its number
    wipe_animation("Select a food item by entering its number: 1 for the first, 2 for the second, etc.")
    description_num = input("-> ")
    expand_animation("===========================================================================================================================")

    # Checking if the input given is valid or not
    try:
        # If the input number is greater than the length of descriptions or less than or equal to 0, raise an error
        if int(description_num) > len(description) or int(description_num) <= 0:
            raise ValueError("invalid item number!")

        # If everything is okay, call print_the_data() on the selected food
        print_the_data(foods, description, description_num, is_branded_food)
        return

    # Handle the exception for invalid input
    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        # Call the function recursively to prompt the user again
        ask_description_num(description, foods, is_branded_food)


def print_the_data(foods, description, description_num, is_branded_food):
    # Iterate through the list of foods
    for food in foods:
        # Check if the current food description matches the given description
        if food["description"] == description[int(description_num)]:
            # Prompt the user with options for displaying nutritional information
            wipe_animation("Enter 'a' for complete nutritional information or 's' for selected nutrients.")
            ask2 = input("-> ")
            expand_animation("===========================================================================================================================")

            try:
                # If the user selects 'a', display complete nutritional information
                if ask2.lower() == "a":
                    # Display branded food data if applicable
                    is_branded_food_data_type(food, is_branded_food)
                    # Display all nutrients
                    print_all_nutrients(food)
                    return
                # If the user selects 's', display specific nutrients
                elif ask2.lower() == "s":
                    # Display branded food data if applicable
                    is_branded_food_data_type(food, is_branded_food)
                    # Display specific nutrients
                    print_specific_nutrients(food)
                    return
                # Raise an exception if the input is not 'a' or 's'
                else:
                    raise ValueError("invalid input!")

            # Handle the exception for invalid input
            except ValueError:
                wipe_animation("Invalid input! Please enter a valid option.")
                expand_animation("===========================================================================================================================")
                # Call the function recursively to prompt the user again
                print_the_data(foods, description, description_num, is_branded_food)


def is_branded_food_data_type(food, is_branded_food):
    # Check if the food item is a branded food
    if is_branded_food:
        # Initialize a list to store the branded food data
        table_data = []
        
        # Append branded food details to the list
        table_data.append(['Description', food["description"]])
        table_data.append(['Brand Name', food["brandName"]])
        table_data.append(['Food Category', food["foodCategory"]])
        table_data.append(['Package Weight', food["packageWeight"]])
        table_data.append(['Serving Size', '100g'])

        # Create a table using the tabulate library
        table = tabulate(table_data, headers=['Attribute', 'Information'], tablefmt="fancy_grid")
        
        # Print the table slowly for better visual effect
        print_slowly(table, 0.0001)
        expand_animation("==========================================================================================================================")
    
    # Return from the function
    return


def print_all_nutrients(food):
    # Display an animation to indicate the beginning of the nutritional values section
    wipe_animation("COMPLETE NUTRITIONAL VALUE")
    print()

    # Initialize lists to store nutrient names and values
    nutrient_name = []
    nutrient_value = []
    
    # Loop through each nutrient in the food item and store its details
    for food_nutrient in food["foodNutrients"]:
        nutrient_name.append(food_nutrient["nutrientName"])
        nutrient_value.append(f'{food_nutrient["value"]}{food_nutrient["unitName"]}')

    # Prepare the data for displaying in a table format
    table_data = list(zip(nutrient_name, nutrient_value))
    
    # Create a table using the tabulate library
    table = tabulate(table_data, headers=['NUTRIENT NAME', 'VALUE/100g'], tablefmt="fancy_grid")
    
    # Print the table slowly for better visual effect
    print_slowly(table, 0.0005)
    
    # Display an animation to indicate the end of the nutritional values section
    expand_animation("==========================================================================================================================")
    
    # Ask the user if they want to restart the process
    ask_want_to_restart()


def print_specific_nutrients(food):
    # Display an animation to indicate the beginning of the nutritional values section
    wipe_animation("COMPLETE NUTRITIONAL VALUE")
    print()
    
    # Initialize lists to store nutrient names, values, and units
    nutrient_names = {}
    nutrient_value = []
    nutrient_value_unit = []
    i = 1
    
    # Loop through each nutrient in the food item and store its details
    for food_nutrient in food["foodNutrients"]:
        nutrient_names[i] = food_nutrient["nutrientName"]
        nutrient_value.append(food_nutrient["value"])
        nutrient_value_unit.append(food_nutrient["unitName"])
        i += 1

    # Prepare the data for displaying in a table format
    table_data = [[key, value] for key, value in nutrient_names.items()]
    
    # Create a table using the tabulate library
    table = tabulate(
        table_data, headers=["S.NO", "NUTRIENT NAME"], tablefmt="fancy_grid"
    )
    
    # Print the table slowly for better visual effect
    print_slowly(table, 0.0005)
    
    # Display an animation to indicate the end of the nutritional values section
    expand_animation("===========================================================================================================================")

    # Ask the user to select a specific nutrient number
    ask_specific_nutrient_num(food, nutrient_names, nutrient_value, nutrient_value_unit)


def ask_specific_nutrient_num(food, nutrient_names, nutrient_value, nutrient_value_unit):
    # Prompt the user with an animation to select a specific nutrient by entering its number
    wipe_animation("Select the specific nutrient by entering its number: 1 for the first, 2 for the second, etc.")
    
    # Get the user's input
    specific_nutrient_num = input("-> ")
    expand_animation("===========================================================================================================================")

    # Checking if the input given is valid or not
    try:
        # If the input number is greater than the length of nutrient_names or less than or equal to 0, raise an error
        if int(specific_nutrient_num) > len(nutrient_names) or int(specific_nutrient_num) <= 0:
            raise ValueError("invalid item number!")

        # If everything is okay, prepare the string with the nutrient information
        printing_string = f"{nutrient_names[int(specific_nutrient_num) - 1]}, {nutrient_value[int(specific_nutrient_num) - 1]}{nutrient_value_unit[int(specific_nutrient_num) - 1].lower()}"
        
        # Display the nutrient information with an animation
        wave_animation(f'{printing_string} in 100g')
        expand_animation("===========================================================================================================================")
        
        # Ask the user if they want to know more about the food
        ask_want_to_know_more(food, nutrient_names, nutrient_value, nutrient_value_unit)

    # Handle the exception for invalid input
    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        # Call the function recursively to prompt the user again
        ask_specific_nutrient_num(food, nutrient_names, nutrient_value, nutrient_value_unit)


def ask_want_to_know_more(food, nutrient_names, nutrient_value, nutrient_value_unit):
    # Prompt the user with an animation to check if they want to see more specific nutritional values for the food
    wipe_animation("Want to see more specific nutritional values for this food? Enter 1 for YES or 0 for NO")
    
    # Get the user's input
    ask = input("-> ")
    expand_animation("===========================================================================================================================")
    
    try:
        # Check if the input is 1 (YES)
        if int(ask) == 1:
            # Call the function to ask for a specific nutrient number
            ask_specific_nutrient_num(food, nutrient_names, nutrient_value, nutrient_value_unit)
            return

        # Check if the input is 0 (NO)
        elif int(ask) == 0:
            # Sleep for a second before restarting the program
            time.sleep(1)
            # Call the function to ask if the user wants to restart the process
            ask_want_to_restart()
            return

        # Raise an exception if the input is not 1 or 0
        else:
            raise ValueError("invalid input!")

    # Handle the exception for invalid input
    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        # Call the function recursively to prompt the user again
        ask_want_to_know_more(food, nutrient_names, nutrient_value, nutrient_value_unit)


def ask_want_to_restart():
    # Prompt the user with an animation to check if they want to check the nutritional values for other foods
    wipe_animation("Do you want to check the nutritional values for other foods? Enter 1 for YES or 0 for NO")

    # Get the user's input
    ask = input("-> ")
    expand_animation("===========================================================================================================================")

    try:
        # Check if the input is 1 (YES)
        if int(ask) == 1:
            # Call the welcome function to restart the process
            welcome()

        # Check if the input is 0 (NO)
        elif int(ask) == 0:
            # Sleep for a second before ending the program
            time.sleep(1)
            #Print a big "End!" message with a burn animation
            print_big("END", burn_animation)
            expand_animation("===========================================================================================================================")
            return

        # Raise an exception if the input is not 1 or 0
        else:
            raise ValueError("invalid input!")

    # Handle the exception for invalid input
    except ValueError:
        wipe_animation("Invalid item number or input! Please enter a valid number.")
        expand_animation("===========================================================================================================================")
        # Call the function recursively to prompt the user again
        ask_want_to_restart()


if __name__ == "__main__":
    # Run the main function if this script is executed directly
    main()
