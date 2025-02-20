# KnowNutritionCLI


https://github.com/user-attachments/assets/87f37a97-ccfb-4fed-97d2-d614c86aaac5


**KnowNutritionCLI** is a simple command-line application that provides detailed nutritional information about foods. It uses data from `USDA FoodData Central`.

## About USDA FoodData Central

**KnowNutritionCLI** relies on [USDA FoodData Central](https://fdc.nal.usda.gov/) for accurate and up-to-date nutritional information. USDA FoodData Central is a reliable source for detailed food and nutrition data.

## Features
- Provides detailed nutritional info about foods using the USDA FoodData Central API.
- Offers an engaging command-line experience with animated text effects.
- Lets users choose to see either full nutritional details or specific nutrients.
- Offers clear instructions and easy options for viewing nutritional details, restarting, or exiting the program.

## Prerequisites

To run this project, you'll need to have the following Python packages installed:

- `requests`
- `pyfiglet`
- `terminaltexteffects`
- `tabulate`
- `python-dotenv`

You can install these packages using `pip`. Here's a command to install all of them at once:

```bash
pip install requests pyfiglet terminaltexteffects tabulate python-dotenv
```

## Installation

To set up and run this project, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/Swapnilgupta8585/know_nutrition_cli
```
2.Navigate to the project directory:
```bash
cd know_nutrition_cli
```

## Setting Up Environment Variables

Before running the program, you need to set up environment variables for your API credentials. Here’s how to do it:

### API Key Setup

To access the nutritional data from USDA FoodData Central, you'll need to obtain an API key. Follow these steps:

1. **Obtain an API Key:**
   - Visit the [USDA FoodData Central API Key Signup](https://fdc.nal.usda.gov/api-key-signup.html) page.
   - Register for an account or log in if you already have one.
   - Follow the instructions to request an API key. After your request is processed, you will receive your API key.

2. **Set Up the `.env` File:**
   - Create a file named `.env` in the root directory of your project.
   - Add the following lines to the `.env` file, replacing `your_api_key_here` with the API key you obtained:

     ```env
     API_KEY=your_api_key_here
     ```

   - Save the `.env` file. This file will be used to load environment variables when running the program.

3. **Example `.env` File:**
   - To help you get started, an example `.env` file (`.env.example`) is included in the repository. It looks like this:

     ```env
     API_KEY=your_api_key_here
     ```

   - Rename `.env.example` to `.env` and update it with your actual API key.

By following these steps, you will configure your environment to securely use the USDA FoodData Central API in your project.

## Running the Application(option1)

After setting up your environment variables and dependencies, you can run the application with the following steps:

1. Ensure main.sh is Executable:

    Make sure that the main.sh script has execution permissions. If not, you can add execute permissions using:
    ```bash 
    chmod +x main.sh
    ```
2. Run the Application:

    Start the application by executing the main.sh script:
    ```bash
    ./main.sh
    ```
## Running the Application(option2)

Alternatively, if you prefer not to use the script, you can run the Python program directly:
```bash
python3 src/main.py
```

Thank You!
