from dotenv import load_dotenv
import requests
import json
import os
import time  # Import the time module

load_dotenv()

# Define the API URL
api_url = "https://opendata.myswitzerland.io/v1/destinations/"

headers = {
    "X-Api-Key": os.getenv("X_API_KEY")
}

responses = []

# Check if responses.json already exists and load its content
if os.path.exists("responses.json"):
    with open("responses.json", "r") as file:
        responses = json.load(file)

# loop through all identifiers.txt and fetch the data
with open("identifiers.txt", "r") as file:
    for identifier in file:
        identifier = identifier.strip()

        # Check if the identifier is already in the responses
        identifier_exists = any(resp.get("data", {}).get("identifier") == identifier for resp in responses)
        if identifier_exists:
            print(f"Data for {identifier} already exists in responses.json. Skipping.")
            continue

        url = api_url + identifier + "?lang=en"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            responses.append(response.json())
            print("Fetched data for " + identifier)
        else:
            print(f"Error fetching data for {identifier}")
            print(response.text)

        time.sleep(1)  # Introduce a 1-second delay before the next request

# save the updated responses to a file
with open("responses.json", "w") as file:
    json.dump(responses, file, indent=2)
