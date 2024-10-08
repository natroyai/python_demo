import requests
import json
from dotenv import load_dotenv
import os
import sys

def load_variables():
     # Load variables from the .env file
    load_dotenv()

    # Initialize the variables dictionary
    variables = {}

    # Add variables from the .env file
    for key, value in os.environ.items():
        variables[key] = value

    # Parse command line arguments
    args = sys.argv[1:]  # Exclude the script name

    # List of required variables

    # Assign arguments to the required variables
    for i, var in enumerate(args):
        if i < len(args):
            variables[var] = args[i]

    return variables

def main():
    variables = load_variables()

    # Check if we have all the necessary variables
    required_vars = ['API_URL', 'API_EMAIL', 'API_PASSWORD']
    for var in required_vars:
        if var not in variables:
            print(f"Error: Missing {var}. Make sure to provide it in .env or as an argument.")
            print("Usage: python script.py API_URL API_EMAIL API_PASSWORD")
            return

    url = variables['API_URL']
    payload = json.dumps({
        "email": variables['API_EMAIL'],
        "password": variables['API_PASSWORD']
    })

    headers = {
        'Content-Type': 'application/json'
    }

    # Send the HTTP POST request
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


if __name__ == "__main__":
    main()
    
    
    