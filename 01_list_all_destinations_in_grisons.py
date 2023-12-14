from dotenv import load_dotenv
import requests
import os

load_dotenv()

# Initialize an empty list to store identifiers
identifiers = []

# Set the initial page number
page_number = 0

# Define the API URL
api_url = "https://opendata.myswitzerland.io/v1/destinations?geo.bbox=47.0651482,8.6510632,46.1691798,10.4922941&page="

headers = {
    "X-Api-Key": os.getenv("X_API_KEY")
}

while True:
    # Construct the URL for the current page
    current_url = api_url + str(page_number)

    # Send a GET request to the API
    response = requests.get(current_url, headers=headers)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()

        # Extract identifiers from the current page and add them to the list
        for item in data.get("data", []):
            identifier = item.get("identifier")
            if identifier:
                identifiers.append(identifier)

        # Check if there are more pages to fetch
        if page_number < data["meta"]["page"]["totalPages"] - 1:
            page_number += 1
        else:
            break
    else:
        print("Error fetching data from the API.")
        break

# save the identifiers to a file
with open("identifiers.txt", "w") as file:
    file.write("\n".join(identifiers))
